from datetime import datetime, timedelta
import jwt
from jwt import ExpiredSignatureError

from src.utils.errors import SDerror


class TokenService:
    def __init__(self, app):
        self.app = app

    def generate_token(self, username, exp, secret):
        payload = {
            "username": username,
            "exp": datetime.utcnow() + timedelta(seconds=int(exp))
        }

        token = jwt.encode(payload, secret, algorithm='HS256').decode('UTF-8')

        return token

    def refresh_token(self, access_token, refresh_token):

        try:
            decoded_access = jwt.decode(access_token, algorithms='HS256', verify=True,
                                        key=self.app.settings['ACCESS_TOKEN_SECRET'], options={"verify_exp": False})

            decoded_refresh = jwt.decode(refresh_token, key=self.app.settings['REFRESH_TOKEN_SECRET'],
                                         algorithms='HS256', verify=True)

        except ExpiredSignatureError as e:
            raise SDerror(
                status_code=401,
                message="Refresh token has expired",
                error_type="JWT Expired Error"
            )

        except Exception as e:
            raise SDerror(
                message="Invalid access token or refresh token",
                error_type="Invalid JWT",
                status_code=400,
                details={"detail": str(e)}
            )

        access_username = decoded_access['username']
        refresh_username = decoded_refresh['username']

        if access_username != refresh_username:
            raise SDerror(
                message="Invalid access token or refresh token.",
                error_type="Invalid JWT",
                status_code=400,
                details={"reason": "Usernames do not match"}
            )

        new_access_token = self.app.token_service.generate_token(access_username,
                                                                 self.app.settings['ACCESS_TOKEN_TTL'],
                                                                 self.app.settings['ACCESS_TOKEN_SECRET'])

        new_refresh_token = self.app.token_service.generate_token(access_username,
                                                                  self.app.settings['REFRESH_TOKEN_TTL'],
                                                                  self.app.settings['REFRESH_TOKEN_SECRET'])

        result = {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

        return result
