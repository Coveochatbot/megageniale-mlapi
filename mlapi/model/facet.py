from json import JSONEncoder


class Facet(JSONEncoder):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_json(self):
        return {"_type": Facet.__name__, "name": self.name, "value": self.value}

    @staticmethod
    def from_json(obj):
        return Facet(obj['name'], obj['value'])
