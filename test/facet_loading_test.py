import unittest
from pathlib import Path
from definitions import Definitions
from mlapi.facet_loader import FacetLoader
from mlapi.model.facet import Facet
import os


class TestFacetLoader(unittest.TestCase):
    TEST_FILE = Path(Definitions.ROOT_DIR + "/test/test_files/facets/temp")

    def test_load_facets(self):
        facet_loader = FacetLoader()
        test_dictionary = self.generate_test_data()

        facet_loader.save_facets(test_dictionary, TestFacetLoader.TEST_FILE)
        facets = facet_loader.load_facets(TestFacetLoader.TEST_FILE)

        self.assertEqual(facets['document1'][0].name, "NameA")
        self.assertEqual(facets['document1'][1].name, "NameB")
        self.assertEqual(facets['document2'][0].name, "NameA")
        self.cleanup_test_file()

    def generate_test_data(self):
        facetA = Facet("NameA", "ValueA")
        facetB = Facet("NameB", "ValueB")
        return {'document1': [facetA, facetB], 'document2': [facetA]}

    def cleanup_test_file(self):
        os.remove(TestFacetLoader.TEST_FILE)





