"""Pynamodb models and helper functions"""
import calendar
import datetime
import os
import time
import uuid
from typing import Dict, List, Optional

from pynamodb.attributes import BooleanAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model

from command import GemsMessage

DATE_FORMAT = "%Y-%m-%d"
THIRTY_ONE_DAYS_IN_SECONDS = 60 * 60 * 24 * 31


class DateIndex(GlobalSecondaryIndex):
    """GSI for date field"""
    date = UnicodeAttribute(hash_key=True)

    class Meta:
        index_name = "date-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = AllProjection()


class GemsModel(Model):
    """Gems table"""
    uuid = UnicodeAttribute(hash_key=True)
    sender = UnicodeAttribute()
    receiver = UnicodeAttribute()
    gem_count = NumberAttribute()
    date = UnicodeAttribute()
    remove_after = NumberAttribute()
    opt_out = BooleanAttribute(default=False)

    date_index = DateIndex()

    class Meta:
        table_name = os.environ["gems_table_name"]
        region = os.environ["AWS_REGION"]


def _scan_with_condition(
        condition,
        last_evaluated_key: Optional[str] = None) -> List[GemsModel]:
    """Scan pynamodb with condition"""
    result = GemsModel.scan(
        condition,
        last_evaluated_key=last_evaluated_key
    )
    items: List[GemsModel] = list(result)

    if result.last_evaluated_key:
        items.extend(
            _scan_with_condition(condition, result.last_evaluated_key)
        )
        return items
    return items


def has_receiver_opted_out(receiver: str):
    """Check if receiver is available"""
    items: List[GemsModel] = _scan_with_condition(
        (GemsModel.sender == receiver) &
        (GemsModel.receiver == receiver) &
        (GemsModel.opt_out == True)
    )
    return len(items) > 0


def insert_opt_out(user: str):
    """Insert an opt-out record in DDB"""
    today = datetime.datetime.today().strftime(DATE_FORMAT)
    remove_after_time = time.time() + THIRTY_ONE_DAYS_IN_SECONDS
    gems = GemsModel(
        uuid=str(uuid.uuid4()),
        sender=user,
        receiver=user,
        gem_count=0,
        opt_out=True,
        date=today,
        remove_after=remove_after_time
    )
    gems.save()
    return remove_after_time


def remove_opt_out(user: str):
    """Remove opt-out record for a user"""
    items: List[GemsModel] = _scan_with_condition(
        (GemsModel.sender == user) &
        (GemsModel.receiver == user) &
        (GemsModel.opt_out == True)
    )
    for item in items:
        item.delete()


def sender_gem_count_today(sender: str):
    """Sender Gem count for today"""

    items: List[GemsModel] = _scan_with_condition(
        (GemsModel.sender == sender) &
        (GemsModel.date == datetime.datetime.today().strftime(DATE_FORMAT))
    )

    total_gems: int = 0
    for item in items:
        total_gems += item.gem_count
    return total_gems


def sender_to_receiver_gem_count_today(sender: str, receiver: str):
    """Sender Gem count for today" given to themselves"""

    items: List[GemsModel] = _scan_with_condition(
        (GemsModel.sender == sender) &
        (GemsModel.receiver == receiver) &
        (GemsModel.date == datetime.datetime.today().strftime(DATE_FORMAT))
    )

    total_gems: int = 0
    for item in items:
        total_gems += item.gem_count
    return total_gems


def get_monthly_rank(month: int, year: int) -> Dict[str, int]:
    last_day: int = calendar.monthrange(year, month)[1]
    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month, last_day)
    items: List[GemsModel] = _scan_with_condition(
        GemsModel.date.between(
            start_date.strftime(DATE_FORMAT),
            end_date.strftime(DATE_FORMAT)
        )
    )

    gems_by_user: Dict[str, int] = dict()
    for item in items:
        gems_by_user[item.receiver] = gems_by_user.get(
            item.receiver, 0) + item.gem_count

    return dict(sorted(gems_by_user.items(), key=lambda x: x[1], reverse=True))


def insert_gem_to_dynamo(gems_message: GemsMessage):
    """Insert gem to dynamo"""
    gems = GemsModel(
        uuid=str(uuid.uuid4()),
        sender=gems_message.sender_discord_id,
        receiver=gems_message.receiver_discord_id,
        gem_count=gems_message.gem_count,
        date=datetime.datetime.today().strftime(DATE_FORMAT),
        remove_after=time.time() + THIRTY_ONE_DAYS_IN_SECONDS
    )
    gems.save()
