import logging
from logging.config import fileConfig
from urllib.parse import quote_plus

from alembic import context
from flask import current_app
from sqlalchemy import create_engine

from api.adapters.database_orm import Base
from api.config import get_db_login

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def get_url():
    try:
        return current_app.config["SQLALCHEMY_DATABASE_URI"]
    except RuntimeError:
        # If Flask app context isn't available, construct URL from config
        username, password, host, port, dbname = get_db_login()
        # URL encode the password to handle special characters
        encoded_password = quote_plus(password)
        return f"postgresql://{username}:{encoded_password}@{host}:{port}/{dbname}"


def get_metadata():
    return Base.metadata


def run_migrations():
    try:
        if context.is_offline_mode():
            run_migrations_offline()
        else:
            run_migrations_online()
    except ValueError:
        # Log sanitized error message
        logger.error("Database URL configuration error")
        # Re-raise with sanitized message
        raise ValueError("Invalid database URL configuration") from None


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Create engine directly with the URL instead of storing in config
    engine = create_engine(get_url())

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    # Create engine directly with the URL
    engine = create_engine(get_url())

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations()
