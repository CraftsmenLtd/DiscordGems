"""Module for accessing the AWS Secrets Manager"""
import os
import urllib.parse

import boto3
import requests
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import GetSecretValueResponseTypeDef


def get_secret(secrets_arn: str) -> str:
    """
        Get secret value from secrets manager

        :param secrets_arn: Name of the secret to get
        :type secrets_arn: str
        :return: secret value
        :rtype: str
    """
    client: SecretsManagerClient = boto3.client(
        service_name="secretsmanager")

    get_secret_value_response: GetSecretValueResponseTypeDef = \
        client.get_secret_value(SecretId=secrets_arn)
    return get_secret_value_response.get("SecretString")


def get_cached_secret(secrets_arn: str) -> str:
    """
        Get secret value from lambda layer

        :param secrets_arn: Name of the secret to get
        :type secrets_arn: str
        :return: secret value
        :rtype: str
    """
    headers = {
        # this function is extremely dependent on the lambda environment
        'X-Aws-Parameters-Secrets-Token':  os.environ['AWS_SESSION_TOKEN']
    }
    param_path = urllib.parse.quote(secrets_arn)

    response = requests.get(
        f'http://localhost:2773/secretsmanager/get?secretId={param_path}', headers=headers)
    response.raise_for_status()

    return response.json()["SecretString"]
