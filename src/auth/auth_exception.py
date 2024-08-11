from fastapi import HTTPException, status


class InvalidData(HTTPException):
    def __init__(self, detail: str, status_code = status.HTTP_401_UNAUTHORIZED):
        super().__init__(detail=detail, status_code=status_code)


class InvalidToken(HTTPException):
    def __init__(self, detail: str, status_code = status.HTTP_403_FORBIDDEN):
        super().__init__(detail=detail, status_code=status_code)