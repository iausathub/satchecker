import json
import os

import boto3
from botocore.exceptions import ClientError


def get_db_login():
    if os.environ.get("DB_HOST") is not None:
        username, password, host, port, dbname = (
            os.environ.get("DB_USERNAME"),
            os.environ.get("DB_PASSWORD"),
            os.environ.get("DB_HOST"),
            os.environ.get("DB_PORT"),
            os.environ.get("DB_NAME"),
        )
        return [username, password, host, port, dbname]

    secret_name = "satchecker-prod-db-cred"  # noqa: S105

    secrets = get_secret(secret_name)
    # Decrypts secret using the associated KMS key.
    username = secrets["username"]
    password = secrets["password"]
    host = secrets["host"]
    port = secrets["port"]
    dbname = secrets["dbname"]

    return [username, password, host, port, dbname]


def get_spacetrack_login():
    secret_name = "spacetrack-login"  # noqa: S105
    try:
        secrets = get_secret(secret_name)
        return secrets["username"], secrets["password"]
    except Exception:
        # if not using secrets manager, try environment variables
        username = os.environ.get("SPACETRACK_USERNAME")
        password = os.environ.get("SPACETRACK_PASSWORD")
        if username is None and password is None:
            # for manual testing, change these values to your spacetrack login
            return "email", "password"
        else:
            return username, password


def get_secret(secret_name):
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    get_secret_value_response = None
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    if get_secret_value_response is None:
        raise RuntimeError("No secret value response")
    secrets = json.loads(get_secret_value_response["SecretString"])

    return secrets
