from flask.json import JSONEncoder
from mlapi.model.question import Question
from mlapi.model.document import Document


class MLJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Question):
            return {
                'text': obj.text
            }
        elif isinstance(obj, Document):
            return {
                'Title': obj.title,
                'Uri': obj.uri,
                'PrintableUri': obj.printableUri,
                'Summary': obj.summary,
                'Excerpt': obj.excerpt
            }

        return super(MLJsonEncoder, self).default(obj)
