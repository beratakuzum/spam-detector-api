import pickle

from src import create_app
from src.utils.general import load_settings_from_environment

if __name__ == '__main__':
    settings = load_settings_from_environment()
    app = create_app(settings)

    model = pickle.load(open('trained-models/spam-detector-model.pickle', 'rb'))
    app.prediction_model = model

    app.run(
        host=settings.get('HOST'),
        port=settings.get('PORT'),
        debug=settings.get('DEBUG')
    )
