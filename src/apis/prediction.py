from flask import jsonify
from src.utils.jwt_auth import authorized


def init_api(app):
    @app.route("/api/prediction/<user_id>", methods=['GET'])
    @authorized(app)
    def register(user_id):

        response_body = app.prediction_service.predict(user_id=user_id)

        return jsonify(response_body), 200
