import fastjsonschema

from src.utils.errors import SDerror
from src.utils.json_helpers import validate_body
from src.apis.json_schemas.auth import REGISTER_SCHEMA

from flask import request, jsonify

REGISTER_SCHEMA_BODY_VALIDATOR = fastjsonschema.compile(REGISTER_SCHEMA)


def init_api(app):
    @app.route("/api/register", methods=['POST'])
    def register_api_user():
        body = request.json
        validate_body(body, REGISTER_SCHEMA_BODY_VALIDATOR)

        username = body['username']
        password = body['password']
        is_username_ascii = username.isascii()
        is_password_ascii = password.isascii()

        if is_password_ascii == False or is_username_ascii == False:
            raise SDerror(
                message="Invalid username or password provided. Username and password can only contain ascii chars",
                status_code=400,
                error_type="Character Error"
            )

        response_body = app.register_service.register(username=username, password=password)

        return jsonify(response_body), 201

    @app.route("/api/login", methods=['GET'])
    def login_api_user():
        args = request.args

        username = args.get('username')
        password = args.get('password')

        if username is None:
            raise SDerror(
                message="Username Not Provided",
                status_code=400,
                error_type="Login Error"
            )

        if password is None:
            raise SDerror(
                message="Password Not Provided",
                status_code=400,
                error_type="Login Error"
            )

        is_username_ascii = username.isascii()
        is_password_ascii = password.isascii()

        if is_password_ascii == False or is_username_ascii == False:
            raise SDerror(
                message="Invalid username or password provided. Username and password can only contain ascii chars",
                status_code=400,
                error_type="Character Error"
            )

        response_body = app.login_service.login(username=username, password_from_client=password)

        return jsonify(response_body), 200

    @app.route("/api/refresh-token", methods=['GET'])
    def token_refresh():
        headers = request.headers
        access_token = headers.get('access_token')
        refresh_token = headers.get('refresh_token')

        if access_token is None or refresh_token is None:
            raise SDerror(
                message="Access Token or Refresh Token Not Provided",
                status_code=400,
                error_type="Token Error"
            )

        body = app.token_service.refresh_token(access_token=access_token, refresh_token=refresh_token)
        return body
