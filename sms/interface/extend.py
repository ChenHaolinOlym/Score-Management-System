from flask_marshmallow.sqla import HyperlinkRelated as OriginalHyperlinkRelated

# Extend HyperLinkRelated to make it able to represent relationship
class HyperlinkRelated(OriginalHyperlinkRelated):
    def __init__(self, rel, endpoint, url_key="id", external=False, **kwargs):
        super().__init__(endpoint, url_key=url_key, external=external, **kwargs)
        self.rel = rel
        if self.rel != "One" and self.rel != "Many":
            raise ValueError('Rel can only be "One" or "Many"')

    def _serialize(self, value, attr, obj):
        url = super()._serialize(value, attr, obj)
        # TODO: Modify according to MS Guideline
        return {
            "rel": self.rel,
            "href": url
        }