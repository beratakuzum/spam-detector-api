import os
import logging

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)


def parse_boolean(value):
    if type(value) is str:
        if value.lower() == 'true':
            return True

        elif value.lower() == 'false':
            return False

    return value


def load_settings_from_environment():
    load_dotenv()
    settings = {}
    for key, value in os.environ.items():
        settings[key] = value

    return settings
