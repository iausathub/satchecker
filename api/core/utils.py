import boto3
from botocore.exceptions import ClientError
import json

def get_db_login():

    secret_name = "satchecker-prod-db-cred"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = None
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        username, password, host, port, dbname = "postgres", "sat123", "localhost", "5432", "postgres"
        return[username, password, host, port, dbname]

    if(get_secret_value_response is None):
        raise Exception("No secret value response")
    
    secrets = json.loads(get_secret_value_response['SecretString'])
    # Decrypts secret using the associated KMS key.
    username = secrets['username']
    password = secrets['password']
    host = secrets['host']
    port = secrets['port']
    dbname = secrets['dbname']

    return[username, password, host, port, dbname]