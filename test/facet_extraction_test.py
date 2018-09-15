import unittest
from mlapi.facet_extractor import FacetExtractor
from definitions import Definitions
from pathlib import Path
from mlapi.model.facet import Facet


class TestFacetExtractor(unittest.TestCase):
    TEST_FILE_A = Path(Definitions.ROOT_DIR + "/test/test_files/facet_extraction_test_file_a.json")
    TEST_FILE_B = Path(Definitions.ROOT_DIR + "/test/test_files/facet_extraction_test_file_b.json")

    def test_simple_facet_extraction(self):
        expected_facet = Facet("spacekey", "Connector")

        actual_facet = FacetExtractor.extract_facet_from_file(TestFacetExtractor.TEST_FILE_A)

        self.assertEqual(expected_facet.name, actual_facet.name)
        self.assertEqual(expected_facet.value, actual_facet.value)

    def test_facet_extraction_from_file_list(self):
        expected_facet_a = Facet("spacekey", "Connector")
        expected_facet_b = Facet("testfacet", "ILoveDogs")
        files = [TestFacetExtractor.TEST_FILE_A, TestFacetExtractor.TEST_FILE_B]

        actual_facets = FacetExtractor.get_facets_from_file(files)

        self.assertEqual(expected_facet_a.name, actual_facets[0].name)
        self.assertEqual(expected_facet_a.value, actual_facets[0].value)
        self.assertEqual(expected_facet_b.name, actual_facets[1].name)
        self.assertEqual(expected_facet_b.value, actual_facets[1].value)
