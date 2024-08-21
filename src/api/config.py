# pragma: no cover
import json
import os

import boto3


def get_db_login():
    """
    Retrieves database login credentials from environment variables or AWS Secrets
    Manager.

    This function first checks if the 'LOCAL_DB' environment variable is set to '1'.
     If it is, it returns a predefined set of local database credentials.

    If 'LOCAL_DB' is not set to '1', it then checks if the 'DB_HOST' environment
    variable is set. If it is, it returns the database credentials from the
    'DB_USERNAME', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', and 'DB_NAME'
    environment variables.

    If neither 'LOCAL_DB' nor 'DB_HOST' are set, it attempts to retrieve the database
    credentials from AWS Secrets Manager. If it fails to retrieve the credentials
    from Secrets Manager, it falls back to the predefined local database credentials.

    Returns:
        list: A list containing the username, password, host, port, and database name,
        in that order.
    """
    if os.environ.get("LOCAL_DB") == "1":
        username, password, host, port, dbname = (
            "postgres",
            "postgres",
            "localhost",
            "5432",
            "satchecker_test",
        )
        return [username, password, host, port, dbname]

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
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    get_secret_value_response = None
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        username, password, host, port, dbname = (
            "postgres",
            "postgres",
            "localhost",
            "5432",
            "satchecker_test",
        )
        return [username, password, host, port, dbname]

    if get_secret_value_response is None:
        raise RuntimeError("No secret value response")

    secrets = json.loads(get_secret_value_response["SecretString"])
    # Decrypts secret using the associated KMS key.
    username = secrets["username"]
    password = secrets["password"]
    host = secrets["host"]
    port = secrets["port"]
    dbname = secrets["dbname"]

    return [username, password, host, port, dbname]
