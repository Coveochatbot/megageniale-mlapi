import unittest
from mlapi.model.facet import Facet
from mlapi.question_generator import DiscriminatingFacetsAlgo

class TestDiscriminatingFacets(unittest.TestCase):
    def test_when_no_discriminating_facet_then_return_no_facet(self):
        discriminating_algo = DiscriminatingFacetsAlgo()
        facet_a1 = Facet('NameA', 'ValueA1')
        facet_a2 = Facet('NameA', 'ValueA2')
        facet_b = Facet('NameB', 'ValueB')
        facets_by_document = {'1': [facet_a1], '2': [facet_a2], '3': [facet_b]}

        discriminating_facets = discriminating_algo.get_discriminating_facets(facets_by_document)
        self.assertEqual(len(discriminating_facets), 0)

    def test_when_1_discriminating_facet_then_return_1_facet(self):
        discriminating_algo = DiscriminatingFacetsAlgo()
        facet_a1 = Facet('NameA', 'ValueA1')
        facet_a2 = Facet('NameA', 'ValueA2')
        facet_b = Facet('NameB', 'ValueB')
        facets_by_document = {'1': [facet_a1], '2': [facet_a2], '3': [facet_a2], '4': [facet_b]}

        discriminating_facets = discriminating_algo.get_discriminating_facets(facets_by_document)
        self.assertEqual(len(discriminating_facets), 1)
        self.assertEqual(discriminating_facets["NameA"], ['ValueA1', 'ValueA2'])

    def test_when_2_discriminating_facets_then_return_2_facet(self):
        discriminating_algo = DiscriminatingFacetsAlgo()
        facet_a1 = Facet('NameA', 'ValueA1')
        facet_a2 = Facet('NameA', 'ValueA2')
        facet_b = Facet('NameB', 'ValueB')
        facet_c1 = Facet('NameC', 'ValueC1')
        facet_c2 = Facet('NameC', 'ValueC2')
        facet_c3 = Facet('NameC', 'ValueC3')
        facets_by_document = {'1': [facet_a1], '2': [facet_a2, facet_c1], '3': [facet_a1, facet_c2, facet_c3], '4': [facet_b, facet_c3]}

        discriminating_facets = discriminating_algo.get_discriminating_facets(facets_by_document)
        self.assertEqual(len(discriminating_facets), 2)
        self.assertEqual(discriminating_facets["NameA"], ['ValueA1', 'ValueA2'])
        self.assertEqual(discriminating_facets["NameC"], ['ValueC1', 'ValueC2', 'ValueC3'])