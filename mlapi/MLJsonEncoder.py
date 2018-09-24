from flask.json import JSONEncoder
from mlapi.model.question import Question


class MLJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Question):
            return {
                'text': obj.text
            }

        return super(MLJsonEncoder, self).default(obj)
