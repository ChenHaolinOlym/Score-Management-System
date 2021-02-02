from flask_restful import Api as OriginalApi
from werkzeug.exceptions import HTTPException

# Extend original Api class to enable customize exceptions
class Api(OriginalApi):
    def error_router(self, original_handler, e):
        if self._has_fr_route() or isinstance(e, HTTPException):
            try:
                return self.handle_error(e)
            except Exception:
                pass  # Fall through to original handler
        return original_handler(e)

class ApiGeneralException(Exception):
    def __init__(self, message:str, code:int=500) -> None:
        Exception.__init__(self)
        self.status = False
        self.message = message
        self.code = code

    def to_dict(self) -> dict:
        return {
            "success": self.status,
            "code": self.code,
            "data": {},
            "message": self.message
        }




api = Api()
