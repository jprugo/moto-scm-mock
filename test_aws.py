from moto import mock_secretsmanager
import pytest
import random

from utils import get_aws_secret_values, get_aws_stack_secrets


@pytest.fixture(scope='function')
@mock_secretsmanager
def mock_secretsmanager_client():
    import boto3
    conn = boto3.client('secretsmanager')
    return conn

@mock_secretsmanager
def mock_create_secret(mock_secretsmanager_client, secrets: list):
    for secret in secrets:
        mock_secretsmanager_client.create_secret(
            Name=secret['name'],
            SecretString=secret['value'],
        )


@mock_secretsmanager
def test_secrets(mock_secretsmanager_client):

    result = get_aws_stack_secrets()

    result = get_aws_secret_values(result)

    secret = random.choice(result)

    mock_create_secret(mock_secretsmanager_client, result)

    response = mock_secretsmanager_client.get_secret_value(
        SecretId=secret['name'],
    )

    print(response)
