from transport.sanic.config import SanicConfig
from db.config import SQLiteConfig, PostgresConfig


class ApplicationConfig:
    sanic: SanicConfig
    database: PostgresConfig

    def __init__(self):
        self.sanic = SanicConfig()
        self.database = PostgresConfig()
