from src.utils.errors import SDerror


class LoginService:
    def __init__(self, app):
        self.app = app

    def login(self, username, password_from_client):
        user = self.app.mongodb_service.find_one('api_users', {'username': username}, {"password": 1})
        if not user:
            raise SDerror(
                message='User not found',
                error_type='Login Error',
                status_code=404
            )

        password_in_db = user['password']
        decrypted_pass = self.app.password_encryption_service.decrypt_password(password_in_db)

        if decrypted_pass != password_from_client:
            raise SDerror(
                message='Wrong Password',
                error_type='Password Error',
                status_code=404
            )

        access_token = self.app.token_service.generate_token(username, self.app.settings['ACCESS_TOKEN_TTL'],
                                                             self.app.settings['ACCESS_TOKEN_SECRET'])

        refresh_token = self.app.token_service.generate_token(username, self.app.settings['REFRESH_TOKEN_TTL'],
                                                              self.app.settings['REFRESH_TOKEN_SECRET'])

        result = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": str(user['_id'])
        }

        return result
