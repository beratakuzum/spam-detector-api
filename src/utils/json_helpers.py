from fastjsonschema import JsonSchemaException

from src.utils.errors import SDerror


def validate_body(data, validator):
    try:
        validator(data)

    except JsonSchemaException as e:
        raise SDerror(
            message="Invalid request body",
            status_code=400,
            error_type="JsonSchemaException",
            details={
                "detail": e.message
            }
        )