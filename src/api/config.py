import os

# Store FOV async task status/results in Postgres (shared across all replicas)
# alongside the Celery/Redis result backend. Each pod has its own Redis sidecar,
# so a task submitted on pod A is invisible to AsyncResult on pod B - without
# this, a status poll load-balanced to a different pod reports PENDING forever.
# Once a single shared Redis backend is available to every replica, set this to
# False (or export FOV_RESULT_STORE_IN_DB=false) to go back to the Redis-only
# polling path; that's the only change needed.
FOV_RESULT_STORE_IN_DB = os.getenv("FOV_RESULT_STORE_IN_DB", "true").lower() == "true"

# How long to keep async FOV task rows before the scheduled cleanup job prunes
# them. Matches the Celery/Redis ``result_expires`` default (24h) the per-pod
# result backend used before results moved to Postgres.
FOV_RESULT_RETENTION_HOURS = int(os.getenv("FOV_RESULT_RETENTION_HOURS", "24"))


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

    Raises:
        RuntimeError: If the database configuration is not found in the environment
        variables and the local database credentials are not set.
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
            os.environ.get("DB_USERNAME", ""),
            os.environ.get("DB_PASSWORD", ""),
            os.environ.get("DB_HOST", ""),
            os.environ.get("DB_PORT", ""),
            os.environ.get("DB_NAME", ""),
        )
        return [username, password, host, port, dbname]

    raise RuntimeError(
        "Database configuration not found. Set either LOCAL_DB=1 or "
        "provide DB_HOST and related environment variables."
    )
