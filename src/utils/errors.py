from flask import jsonify


# SDerror means spam detector error
class SDerror(Exception):

    def __init__(self, message, status_code, error_type, details=None):
        Exception.__init__(self)
        self.err_message = message
        self.status_code = status_code
        self.details = details
        self.err_type = error_type

    def to_dict(self):
        payload = {
            'message': self.err_message,
            'error_type': self.err_type,
            'code': self.status_code,
        }
        if self.details is not None:
            payload['details'] = self.details

        return payload


def init_error_handler(app):
    @app.errorhandler(SDerror)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
