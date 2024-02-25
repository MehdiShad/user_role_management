from rest_framework.exceptions import ValidationError


class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}

def handle_validation_error(serializer):
    try:
        serializer.is_valid(raise_exception=True)
        return True  # Validation successful
    except ValidationError as ve:
        if (len(ve.detail.items())) == 1:
            error_message = next(iter(ve.detail.values()))[0]
            response_data = {
                "is_success": False,
                "data": {
                    "error_type": "",
                    "params": list(ve.detail.keys())[0],
                    "message": error_message,
                }
            }

        else:
            error_messages = ""
            error_type = ""
            for key, values in ve.detail.items():
                error_type += str(key) + " "
                error_messages += f"{str(key)}: {str(values[0])} "
            response_data = {
                "is_success": False,
                "data": {
                    "error_type": "",
                    "params": error_type,
                    "message": error_messages,
                }
            }

        return response_data


def error_response(
        *,
        error_type: str = "",
        params: str = "",
        message: str = "",
):
    return {
        "is_success": False,
        "data": {
            "error_type": error_type,
            "params": params,
            "message": message,
        }
    }


def success_response(
        *,
        data: dict = {},
):
    return {
        "is_success": True,
        "data": data
    }