import unittest
from mlapi.facet_extractor import FacetExtractor
from definitions import Definitions
from pathlib import Path


class TestFacetExtractor(unittest.TestCase):
    TEST_FILE_A = Path(Definitions.ROOT_DIR + "/test/test_files/facets/facet_extraction_test_file_a.json")
    TEST_FILE_B = Path(Definitions.ROOT_DIR + "/test/test_files/facets/facet_extraction_test_file_b.json")

    def test_get_facets_by_document(self):
        extractor = FacetExtractor()

        my_dic = extractor.get_facets_by_document([TestFacetExtractor.TEST_FILE_A, TestFacetExtractor.TEST_FILE_B])

        self.assertEqual(my_dic['Document3'][0].name, "FacetA")
        self.assertEqual(my_dic['Document1'][0].name, "FacetA")
        self.assertEqual(my_dic['Document1'][1].name, "FacetB")
        self.assertEqual(my_dic['Document2'][0].name, "FacetB")

    def test_invert_dictionary(self):
        my_dic = {"A": ["1", "2"], "B": ["1"]}

        inv_dic = FacetExtractor.invert_dictionary(my_dic)

        self.assertEqual(inv_dic["1"][0], "A")
        self.assertEqual(inv_dic["1"][1], "B")
        self.assertEqual(inv_dic["2"][0], "A")

    def test_extract_facet_from_file(self):
        facet, document_uris = FacetExtractor.extract_facet_from_file(TestFacetExtractor.TEST_FILE_A)

        self.assertEqual(facet.name, "FacetA")
        self.assertEqual(facet.value, "FacetValueA")
        self.assertEqual(document_uris[0], "Document3")
        self.assertEqual(document_uris[1], "Document1")
