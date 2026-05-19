from rest_framework.exceptions import APIException


class DockedServiceError(APIException):
    status_code = 502
    default_detail = "Data Docked API request failed."
    default_code = "docked_error"

    def __init__(self, detail=None, status_code=None):
        if detail is not None:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code
