from flask_restful import Api as OriginalApi
from flask_marshmallow.sqla import HyperlinkRelated as OriginalHyperlinkRelated

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

# Extend base exception to allow customize exception to pass flask_restful's interceptor
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

# Extend HyperLinkRelated to make it able to represent relationship
class HyperlinkRelated(OriginalHyperlinkRelated):
    def __init__(self, rel, endpoint, url_key="id", external=False, **kwargs):
        super().__init__(endpoint, url_key=url_key, external=external, **kwargs)
        self.rel = rel
        if self.rel != "One" and self.rel != "Many":
            raise ValueError('Rel can only be "One" or "Many"')

    def _serialize(self, value, attr, obj):
        url = super()._serialize(value, attr, obj)
        return {
            "rel": self.rel,
            "href": url
        }