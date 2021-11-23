from moto import mock_secretsmanager
import pytest
import random
import os
import boto3

from utils import get_aws_secret_values, get_aws_stack_secrets


@pytest.fixture(scope='function')
def mock_secretsmanager_client():
    with mock_secretsmanager():
        yield boto3.client('secretsmanager')


@mock_secretsmanager
def mock_create_secret(mock_secretsmanager_client, secrets: list):
    for secret in secrets:
        mock_secretsmanager_client.create_secret(
            Name=secret['name'],
            SecretString=secret['value'],
        )


@pytest.fixture
def test_function(env_var):
    return env_var


@pytest.mark.parametrize('env_var',[os.environ['test']])
def test_env_var_fixture(test_function):
    assert test_function == os.environ['test']


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


