from cryptography.fernet import Fernet


class PassWordEncryptionService:
    def __init__(self, app):
        self.fernet = Fernet(app.settings['PASS_KEY'])

    def encrypt_password(self, password):
        encoded_password = password.encode()
        encrypted_password = self.fernet.encrypt(encoded_password)

        return encrypted_password.decode("utf-8")

    def decrypt_password(self, encrypted_password):
        encoded_encrypted_password = encrypted_password.encode()
        decrypted_password_bytes = self.fernet.decrypt(encoded_encrypted_password)

        return decrypted_password_bytes.decode("utf-8")