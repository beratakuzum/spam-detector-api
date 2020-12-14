
def init_apis(app):
    from .auth import init_api
    init_api(app=app)

    from .prediction import init_api
    init_api(app=app)
