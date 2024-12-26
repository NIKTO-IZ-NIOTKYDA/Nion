class BackendAPIError(Exception):
    pass


class NoResponseFromServer(BackendAPIError):
    pass


class ResponseError(BackendAPIError):
    status: str = None
    details: str = None

    def __init__(self, response_json: dict) -> None:
        super().__init__()

        self.status = response_json['status']
        self.details = response_json['details']