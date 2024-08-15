from datetime import datetime
import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

sys.path.append(os.path.join(sys.path[0], "src"))
from settings import settings_obj
from models import BaseModelORM

config.set_main_option("sqlalchemy.url", settings_obj.database_url)
target_metadata = BaseModelORM.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    def process_revision_directives(context, revision, directives):
        # 20240101_21_10_24 for a migration generated on 1st January, 2024 at 21:10:24
        rev_id = datetime.now().strftime("%Y%m%d_%H_%M_%S")
        for directive in directives:
            directive.rev_id = rev_id

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            process_revision_directives=process_revision_directives,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
