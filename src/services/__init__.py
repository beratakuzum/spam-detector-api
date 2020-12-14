from .mongodb import MongoDbService
from .password_encryption import PassWordEncryptionService
from .register import RegisterService
from .token_service import TokenService
from .login import LoginService
from .prediction import PredictorService


def init_services(app):
    app.mongodb_service = MongoDbService(db_name='spam_detector')
    app.password_encryption_service = PassWordEncryptionService(app=app)
    app.register_service = RegisterService(app=app)
    app.token_service = TokenService(app=app)
    app.login_service = LoginService(app=app)
    app.prediction_service = PredictorService(app=app)