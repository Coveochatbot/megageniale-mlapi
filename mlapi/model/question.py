class Question(object):

    def __init__(self, text):
        self.text = text

    def to_json(self):
        return {"text": self.text}
