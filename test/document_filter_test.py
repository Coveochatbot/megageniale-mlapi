import unittest

from mlapi.document_filter import DocumentFilter
from mlapi.model.facet import Facet


class TestDocumentFilter(unittest.TestCase):
    # Must have section

    def test_must_have_facet_a(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_with_facets(self.generate_data(), [Facet("FacetA", "FacetValueA")])

        self.assertEqual(3, len(documents))
        self.assertTrue("Document1" in documents)
        self.assertTrue("Document2" not in documents)
        self.assertTrue("Document3" in documents)
        self.assertTrue("Document4" in documents)
        self.assertTrue("Document5" not in documents)

    def test_must_have_facet_d(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_with_facets(self.generate_data(), [Facet("FacetD", "FacetValueD")])

        self.assertEqual(0, len(documents))
        self.assertTrue("Document1" not in documents)
        self.assertTrue("Document2" not in documents)
        self.assertTrue("Document3" not in documents)
        self.assertTrue("Document4" not in documents)
        self.assertTrue("Document5" not in documents)

    def test_must_have_facet_a_and_b(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_with_facets(self.generate_data(), [Facet("FacetA", "FacetValueA"), Facet("FacetB", "FacetValueB")])

        self.assertEqual(1, len(documents))
        self.assertTrue("Document1" in documents)
        self.assertTrue("Document2" not in documents)
        self.assertTrue("Document3" not in documents)
        self.assertTrue("Document4" not in documents)
        self.assertTrue("Document5" not in documents)

    def test_must_have_facet_a2(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_with_facets(self.generate_data(), [Facet("FacetA", "FacetValueA2")])

        self.assertEqual(2, len(documents))
        self.assertTrue("Document1" not in documents)
        self.assertTrue("Document2" not in documents)
        self.assertTrue("Document3" not in documents)
        self.assertTrue("Document4" in documents)
        self.assertTrue("Document5" in documents)

    # Must NOT have section

    def test_must_not_have_facet_a(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_without_facets(self.generate_data(), [Facet("FacetA", "FacetValueA")])

        self.assertEqual(2, len(documents))
        self.assertTrue("Document1" not in documents)
        self.assertTrue("Document2" in documents)
        self.assertTrue("Document3" not in documents)
        self.assertTrue("Document4" not in documents)
        self.assertTrue("Document5" in documents)

    def test_must_not_have_facet_d(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_without_facets(self.generate_data(), [Facet("FacetD", "FacetValueD")])

        self.assertEqual(5, len(documents))
        self.assertTrue("Document1" in documents)
        self.assertTrue("Document2" in documents)
        self.assertTrue("Document3" in documents)
        self.assertTrue("Document4" in documents)
        self.assertTrue("Document5" in documents)

    def test_must_not_have_facet_a_or_b(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_without_facets(self.generate_data(), [Facet("FacetA", "FacetValueA"), Facet("FacetB", "FacetValueB")])

        self.assertEqual(1, len(documents))
        self.assertTrue("Document1" not in documents)
        self.assertTrue("Document2" not in documents)
        self.assertTrue("Document3" not in documents)
        self.assertTrue("Document4" not in documents)
        self.assertTrue("Document5" in documents)

    def test_must_not_have_facet_a_or_b_chained(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_without_facets(self.generate_data(), [Facet("FacetA", "FacetValueA")])
        documents = document_filter.keep_documents_without_facets(documents, [Facet("FacetB", "FacetValueB")])

        self.assertEqual(1, len(documents))
        self.assertTrue("Document1" not in documents)
        self.assertTrue("Document2" not in documents)
        self.assertTrue("Document3" not in documents)
        self.assertTrue("Document4" not in documents)
        self.assertTrue("Document5" in documents)

    # Must have X and NOT have Y section

    def test_must_not_have_facet_a_and_not_b(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_with_facets(self.generate_data(), [Facet("FacetA", "FacetValueA")])
        documents = document_filter.keep_documents_without_facets(documents, [Facet("FacetB", "FacetValueB")])

        self.assertEqual(2, len(documents))
        self.assertTrue("Document1" not in documents)
        self.assertTrue("Document2" not in documents)
        self.assertTrue("Document3" in documents)
        self.assertTrue("Document4" in documents)
        self.assertTrue("Document5" not in documents)

    def test_must_not_have_facet_a_and_not_b_comutative(self):
        document_filter = DocumentFilter()
        documents = document_filter.keep_documents_without_facets(self.generate_data(), [Facet("FacetB", "FacetValueB")])
        documents = document_filter.keep_documents_with_facets(documents, [Facet("FacetA", "FacetValueA")])

        self.assertEqual(2, len(documents))
        self.assertTrue("Document1" not in documents)
        self.assertTrue("Document2" not in documents)
        self.assertTrue("Document3" in documents)
        self.assertTrue("Document4" in documents)
        self.assertTrue("Document5" not in documents)

    def generate_data(self):
        facetA = Facet("FacetA", "FacetValueA")
        facetA2 = Facet("FacetA", "FacetValueA2")
        facetB = Facet("FacetB", "FacetValueB")
        facetC = Facet("FacetC", "FacetValueC")

        return {'Document1': [facetA, facetB],
                'Document2': [facetB, facetC],
                'Document3': [facetA, facetC],
                'Document4': [facetA2, facetA],
                'Document5': [facetA2, facetC]}
