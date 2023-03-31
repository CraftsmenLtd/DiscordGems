"""Module for accessing the AWS Secrets Manager"""
import boto3
from mypy_boto3_secretsmanager import SecretsManagerClient
from mypy_boto3_secretsmanager.type_defs import GetSecretValueResponseTypeDef


def get_secret(secrets_arn: str) -> str:
    """
        Get secret value from secrets manager

        :param secrets_arn: Name of the secret to get
        :type secrets_arn: str
        :return: secret value in encoded base64
        :rtype: str
        """
    client: SecretsManagerClient = boto3.client(
        service_name="secretsmanager")

    get_secret_value_response: GetSecretValueResponseTypeDef = \
        client.get_secret_value(SecretId=secrets_arn)
    return get_secret_value_response.get("SecretString")
