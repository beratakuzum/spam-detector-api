from flask import Flask


def create_app(settings):
    app = Flask(__name__)
    app.settings = settings

    from src.utils import init_utils
    init_utils(app)

    from .apis import init_apis
    init_apis(app)

    from .services import init_services
    init_services(app)

    return app

