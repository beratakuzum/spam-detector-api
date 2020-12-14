import pandas as pd

from src.utils.errors import SDerror


class PredictorService:
    def __init__(self, app):
        self.app = app
        self.country_indexes = {
            "AM": 11, "AZ": 12, "BR": 13, "BY": 14, "CA": 15, "GE": 16, "ID": 17, "IL": 18, "IN": 19,
            "KR": 20, "KZ": 21, "MX": 22, "MY": 23, "NO": 24, "RU": 25, "SG": 26, "TR": 27, "UA": 28,
            "US": 29
        }

    def predict(self, user_id):
        user = self.app.mongodb_service.find_one('users', {'user_id': user_id}, {"_id": 0})
        if not user:
            raise SDerror(
                message="User Does Not Exist",
                status_code=404,
                error_type="Prediction Error"
            )

        pred_input = self._preprocess_user_data_for_prediction(user_data=user)
        pred = self.app.prediction_model.predict([pred_input])[0]
        if pred == 1:
            result = {
                "user_id": user_id,
                "is_spam": True
            }

        else:
            result = {
                "user_id": user_id,
                "is_spam": False
            }

        return result

    def _preprocess_user_data_for_prediction(self, user_data):
        _data_no_country = [
            1 if user_data['registered_user'] else 0,
            user_data['call_count'],
            user_data['answered_call'],
            user_data['rejected_call'],
            user_data['missed_call'],
            user_data['out_of_work_call'],
            user_data['user_feedback_count'],
            user_data['owertime_call'],
            user_data['total_duration (second)'],
            user_data['weekdays_call'],
            user_data['weekend_call']
        ]

        _data_with_country = _data_no_country + [0 for i in range(19)]
        _data_with_country[self.country_indexes[user_data['country']]] = 1

        return _data_with_country
