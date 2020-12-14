
REGISTER_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'username': {
            "type": "string",
            'minLength': 3,
            'maxLength': 100
        },
        'password': {
            "type": "string",
            'minLength': 5,
            'maxLength': 100
        }
    },
    "additionalProperties": False,
    'required': ['username', 'password']
}