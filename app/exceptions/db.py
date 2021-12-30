class DbConnectionError(Exception):
    def __init__(self, msg: str = "Connection to database failed") -> None:
        self.msg = msg


class DbNotInitialized(Exception):
    def __init__(self, msg: str = "Database client has not been initialized") -> None:
        self.msg = msg


class ModelSchemaError(Exception):
    def __init__(self, msg: str = "The provided model has a schema error or is unsupported") -> None:
        self.msg = msg


class NullQueryResult(Exception):
    def __init__(self, msg: str = "The query returned None") -> None:
        self.msg = msg
