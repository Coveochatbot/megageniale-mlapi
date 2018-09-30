class DocumentFilter(object):

    @staticmethod
    def keep_documents_with_facets(documents, must_have_facets):
        documents_with_facets = {}
        for document, facets in documents.items():
            if set(must_have_facets).issubset(facets):
                documents_with_facets[document] = facets

        return documents_with_facets

    @staticmethod
    def keep_documents_without_facets(documents, must_not_have_facets):
        documents_with_facets = {}
        for document, facets in documents.items():
            if set(must_not_have_facets).isdisjoint(facets):
                documents_with_facets[document] = facets

        return documents_with_facets
