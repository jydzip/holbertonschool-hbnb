def make_error(api, status_code: int, message: str):
    error_msg = f"{status_code} "

    if status_code == 409:
        error_msg += "Conflict"
    elif status_code == 404:
        error_msg += "Not Found"
    elif status_code == 400:
        error_msg += "Bad Request"

    api.abort(status_code, f"{message}", error=error_msg)