from configs.config import ApplicationConfig
from sqlalchemy import create_engine

from db.database import Database
from context import Context


def init_db_sqlite(config: ApplicationConfig, context: Context):
    url = r'sqlite:///db.sqlite'
    engine = create_engine(
        config.database.url,
        pool_pre_ping=True,
    )
    database = Database(connection=engine)
    database.check_connection()

    context.set('database', database)
