"""Module for accessing the AWS Secrets Manager"""

import base64
import binascii
import json
import logging
from typing import Dict, Optional

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import GetSecretValueResponseTypeDef

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class SecretsManagerHelper:
    """Class for accessing the AWS Secrets Manager"""

    def get_secret(self, secret_name: str) -> Optional[Dict[str, str]]:
        """
        Get secret value from secrets manager

        :param secret_name: Name of the secret to get
        :type secret_name: str
        :return: secret value in encoded base64
        :rtype: option[object]
        """
        client: SecretsManagerClient = boto3.client(service_name="secretsmanager")

        try:
            get_secret_value_response: GetSecretValueResponseTypeDef = \
                client.get_secret_value(SecretId=secret_name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "DecryptionFailureException":
                LOGGER.error(
                    "Secrets Manager can't decrypt the protected secret text.")
                LOGGER.error(secret_name)
            elif exc.response["Error"]["Code"] == "InternalServiceErrorException":
                LOGGER.error("An error occurred on the server side.")
                LOGGER.error(secret_name)
            elif exc.response["Error"]["Code"] == "InvalidParameterException":
                LOGGER.error("invalid value provided for a parameter")
                LOGGER.error(secret_name)
            elif exc.response["Error"]["Code"] == "InvalidRequestException":
                LOGGER.error(
                    "parameter is not valid for the current state of the resource")
                LOGGER.error(secret_name)
            elif exc.response["Error"]["Code"] == "ResourceNotFoundException":
                LOGGER.error("Unable to find the specified resource")
                LOGGER.error(secret_name)
            else:
                LOGGER.error("Unexpected or Unknown errors")
            return None
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these
            # fields will be populated.

            secret_string: str = get_secret_value_response.get("SecretString")
            if secret_string is not None:
                return json.loads(secret_string)

            try:
                secret_binary: bytes = get_secret_value_response["SecretBinary"]
                return json.loads(base64.b64decode(secret_binary))
            except (binascii.Error, TypeError, json.decoder.JSONDecodeError, UnicodeDecodeError):
                LOGGER.error("Secret binary decode error")

            LOGGER.error("No secret value found")
            return None
