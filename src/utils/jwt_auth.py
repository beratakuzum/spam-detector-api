from functools import wraps
from src.utils.errors import SDerror

from jwt import ExpiredSignatureError
from flask import request
import jwt


def authorized(app):
    def decorator(f):
        @wraps(f)
        def decorated_function(**kwargs):

            bearer_token = request.headers.get("Authentication")
            if not bearer_token:
                raise SDerror(
                    status_code=400,
                    message="Auth token not provided",
                    error_type="Token Error"
                )

            try:
                decoded = jwt.decode(bearer_token, key=app.settings['ACCESS_TOKEN_SECRET'], algorithms='HS256',
                                     verify=True)

            except ExpiredSignatureError as e:
                raise SDerror(
                    status_code=401,
                    message="Token has expired",
                    error_type="JWT Expired Error",
                    details={
                        "message": str(e)
                    }
                )

            except Exception as e:
                raise SDerror(
                    status_code=400,
                    message="Token invalid",
                    error_type="JWT Validation Error",
                    details={
                        "message": str(e)
                    }
                )
            response = f(**kwargs)
            return response

        return decorated_function

    return decorator
