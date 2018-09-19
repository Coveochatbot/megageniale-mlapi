class Document(object):

    def __init__(self, title, uri, printableUri, summary, excerpt):
        self.title = title
        self.uri = uri
        self.printableUri = printableUri
        self.summary = summary
        self.excerpt = excerpt