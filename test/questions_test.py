import unittest
from mlapi.model.facet import Facet
from mlapi.question_generator import QuestionGenerator


class TestQuestions(unittest.TestCase):
    def test_no_question(self):
        question_generator = QuestionGenerator()
        facetA = Facet('NameA', 'ValueA')
        facets_by_document = {'1': [facetA], '2': [facetA]}

        questions = question_generator.generate_questions(facets_by_document)
        self.assertEqual(len(questions), 0)

    def test_no_facets(self):
        question_generator = QuestionGenerator()
        questions = question_generator.generate_questions([])
        self.assertEqual(len(questions), 0)

    def test_one_element_question(self):
        question_generator = QuestionGenerator()
        facetA = Facet('NameA', 'ValueA')
        facetB = Facet('NameB', 'ValueB')

        facets_by_document = {'1': [facetA, facetB], '2': [facetA]}
        questions = question_generator.generate_questions(facets_by_document)
        self.assertEqual(questions[0].facet_name, "NameB")
        self.assertEqual(sorted(questions[0].facet_values), ['ValueB'])
        self.assertTrue(questions[0].id == 0)

    def test_similar_values_different_facets(self):
        question_generator = QuestionGenerator()
        facetA = Facet('NameA', 'ValueA')
        facetA2 = Facet('NameA', 'ValueA')
        facetB = Facet('NameB', 'ValueB')
        facets_by_document = {'1': [facetA2, facetB], '2': [facetA]}

        questions = question_generator.generate_questions(facets_by_document)
        self.assertEqual(questions[0].facet_name, "NameB")
        self.assertEqual(sorted(questions[0].facet_values), ['ValueB'])
        self.assertTrue(questions[0].id == 0)

    def test_multiple_values_question(self):
        question_generator = QuestionGenerator()
        facetA = Facet('NameA', 'ValueA')
        facetB = Facet('NameA', 'ValueB')
        facetC = Facet('NameB', 'Value1')
        facetD = Facet('NameB', 'Value2')
        facetE = Facet('NameB', 'Value3')
        facets_by_document = {'1': [facetA, facetD, facetE], '2': [facetB, facetC, facetE]}

        questions = sorted(question_generator.generate_questions(facets_by_document), key=lambda x: x.facet_name)
        self.assertEqual(questions[0].facet_name, 'NameA')
        self.assertEqual(sorted(questions[0].facet_values), ['ValueA', 'ValueB'])
        self.assertTrue(questions[0].id == 0 or questions[0].id == 1)
        self.assertEqual(questions[1].facet_name, 'NameB')
        self.assertEqual(sorted(questions[1].facet_values), ['Value1', 'Value2'])
        self.assertTrue(questions[1].id == 0 or questions[1].id == 1)


