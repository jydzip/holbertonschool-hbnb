from flask_restx import Namespace

def make_error(api: Namespace, status_code: int, message: str):
    """
        Creates and returns an error response api.
        Args:
            api (Namespace): Namespace.
            status_code (int): Abort status code for the error: 400, 404 ou 409.
            message (str): Error message to display.
    """
    error_msg = f"{status_code} "

    if status_code == 409:
        error_msg += "Conflict"
    elif status_code == 404:
        error_msg += "Not Found"
    elif status_code == 400:
        error_msg += "Bad Request"

    error_response = {
        "message": message,
        "error": error_msg
    }
    api.abort(status_code, **error_response)