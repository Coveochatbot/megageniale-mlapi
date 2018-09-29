import json
from mlapi.model.facet import Facet


class ObjectDecoder(json.JSONDecoder):
    FROM_JSON_BY_TYPE = {Facet.__name__: Facet.from_json}

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' in obj and obj['_type'] in ObjectDecoder.FROM_JSON_BY_TYPE:
            return ObjectDecoder.FROM_JSON_BY_TYPE[obj['_type']](obj)
        return obj

