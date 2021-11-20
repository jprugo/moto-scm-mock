import boto3

cf = boto3.client('cloudformation')

"""
    Se obtienen los recursos filtrados de un stack, donde se discriminan por solo secretsmanager
"""
def get_aws_stack_secrets():
    response = cf.list_stack_resources(
        StackName='your_stack_name',
    )

    resources = response['StackResourceSummaries']

    secrets = list(
        filter(lambda elem: elem['ResourceType'] == 'AWS::SecretsManager::Secret', resources))

    return secrets

secretsmanager = boto3.client('secretsmanager')

"""
    Deberia retornar una lista de dicccionarios con el nombre del secreto y con su valor confidencial
"""
def get_aws_secret_values(stack_secrets):
    data = []
    for secret in stack_secrets:
        secretId = secret['PhysicalResourceId']
        name = secret['LogicalResourceId']
        value= secretsmanager.get_secret_value(
            SecretId=secretId,
        )['SecretString']
        data.append(
            {
                "id": secretId,
                "name": name,
                "value": value
            }
        )
    return data

