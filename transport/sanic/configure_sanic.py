from sanic import Sanic
from configs.config import ApplicationConfig
from context import Context
from transport.sanic.routes import get_routes
from hooks import init_db_sqlite


def configure_app(config: ApplicationConfig, context: Context):
    app = Sanic(__name__)

    init_db_sqlite(config, context)

    for handler in get_routes(config, context):
        app.add_route(
            handler=handler,
            uri=handler.uri,
            methods=handler.methods,
            strict_slashes=True
        )

    return app
