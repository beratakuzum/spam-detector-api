from src.utils.errors import SDerror


class RegisterService:
    def __init__(self, app):
        self.app = app

    def register(self, username, password):
        user = self.app.mongodb_service.find_one('api_users', {'username': username})
        if user:
            raise SDerror(
                message="User Already exists",
                status_code=409,
                error_type="User Creation Error"
            )

        encrypted_pass = self.app.password_encryption_service.encrypt_password(password)
        access_token = self.app.token_service.generate_token(username, self.app.settings['ACCESS_TOKEN_TTL'],
                                                             self.app.settings['ACCESS_TOKEN_SECRET'])

        refresh_token = self.app.token_service.generate_token(username, self.app.settings['REFRESH_TOKEN_TTL'],
                                                              self.app.settings['REFRESH_TOKEN_SECRET'])

        doc = {
            'username': username,
            'password': encrypted_pass
        }

        inserted_user = self.app.mongodb_service.insert_one('api_users', doc)
        user_id = inserted_user.inserted_id

        result = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": str(user_id)
        }

        return result
