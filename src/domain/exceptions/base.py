class ProblemDetailsException(Exception):
    def __init__(
        self, *, type_uri: str, title: str, status: int, detail: str, instance: str | None = None
    ):
        self.type_uri = type_uri
        self.title = title
        self.status = status
        self.detail = detail
        self.instance = instance
        super().__init__(detail)
