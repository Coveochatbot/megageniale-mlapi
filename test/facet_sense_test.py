import unittest
from mlapi.facet_sense_analyzer import FacetSenseAnalyzer
from mlapi.facet_sense_api import FacetSenseApi
from unittest.mock import MagicMock
import json


class TestFacetSense(unittest.TestCase):

    def test_conversion_to_facet_from_valid_json(self):
        facet_sense_api = FacetSenseApi()
        test_data = self.generate_valid_test_data()
        facet_sense_analyzer = FacetSenseAnalyzer(facet_sense_api)

        result = facet_sense_analyzer.content_to_facet_dto(json.loads(test_data))

        first_facet = result[0]
        values = first_facet.values
        self.assertEqual(first_facet.name, 'facetNameA')
        self.assertEqual(first_facet.score, 100)
        self.assertEqual(values[0].value, 'ValueA')
        self.assertEqual(values[0].score, 48)
        self.assertEqual(values[1].value, 'ValueB')
        self.assertEqual(values[1].score, 47)

    def test_conversion_to_facet_from_empty_json(self):
        facet_sense_api = FacetSenseApi()
        facet_sense_analyzer = FacetSenseAnalyzer(facet_sense_api)

        result = facet_sense_analyzer.content_to_facet_dto(json.loads("{}"))

        self.assertEqual(len(result), 0)

    def test_facet_sense_with_valid_json_returns_valid_dto(self):
        facet_sense_api = FacetSenseApi()
        test_data = self.generate_valid_test_data()
        facet_sense_api.get_facet_scores = MagicMock(return_value=test_data)
        facet_sense_analyzer = FacetSenseAnalyzer(facet_sense_api)

        result = facet_sense_analyzer.analyse("test text")

        first_facet = result[0]
        values = first_facet.values
        self.assertEqual(first_facet.name, 'facetNameA')
        self.assertEqual(first_facet.score, 100)
        self.assertEqual(values[0].value, 'ValueA')
        self.assertEqual(values[0].score, 48)
        self.assertEqual(values[1].value, 'ValueB')
        self.assertEqual(values[1].score, 47)

    def generate_valid_test_data(self):
        return "{\"facets\": [{\"id\":\"facetNameA\",\"score\":100,\"facetValues\":[{\"value\": \"ValueA\", " \
               "\"score\":48},{\"value\": \"ValueB\", \"score\":47}]}]}"


