import unittest

from mlapi.analytics.get_suggested_documents_from_past_searches import get_words_and_parts_of_speech, \
    get_searches_containing_context_entities, get_searches_scores, get_searches_relative_scores


class TestIdentifyWordsInSearches(unittest.TestCase):
    def test_get_searches_containing_context_entities_find_searches_with_at_least_one_same_word(self):
        searches_documents_mapping = {
            "i am a key": [
                "i am a link"
            ],
            "another key": [
                "another link"
            ],
            "no same word": [
                "another link"
            ]
        }
        context_entities = {"key"}
        expected_result = {
            "i am a key": {
                "key"
            },
            "another key": {
                "key"
            }
        }
        actual_result = get_searches_containing_context_entities(searches_documents_mapping, context_entities)
        self.assertEqual(actual_result, expected_result)

    def test_get_searches_containing_context_entities_returns_all_same_words(self):
        searches_documents_mapping = {
            "i am a key": [
                "i am a link"
            ],
            "another key": [
                "another link"
            ],
            "no same word": [
                "another link"
            ]
        }
        context_entities = {"key", "another", "a"}
        expected_result = {
            "i am a key": {
                "key",
                "a"
            },
            "another key": {
                "key",
                "another"
            }
        }
        actual_result = get_searches_containing_context_entities(searches_documents_mapping, context_entities)
        self.assertEqual(actual_result, expected_result)

    def test_identify_words_in_searches(self):
        test_search = ["throw", "your", "banana"]
        expected_results = {
            "banana": "NN",
            "your": "PRP$",
            "throw": "VB"
        }
        self.assertEqual(get_words_and_parts_of_speech(test_search), expected_results)

    def test_get_search_score(self):
        searches_containing_context_entities = {
            "throw your banana": {
                "throw",
                "banana"
            },
            "you love banana": {
                "banana",
                "you"
            }
        }
        parts_of_speech_scores = {
            "NN": 5,
            "NNS": 5,
            "VB": 2,
            "VBP": 2,
            "PRP": 2
        }
        expected_search_scores = {
            "throw your banana": 7,
            "you love banana": 7
        }
        self.assertEqual(
            expected_search_scores,
            get_searches_scores(searches_containing_context_entities, parts_of_speech_scores)
        )

    def test_get_search_score_with_duplicates_only_counts_word_once(self):
        searches_containing_context_entities = {
            "throw your banana and banana": {
                "throw",
                "banana"
            }
        }
        parts_of_speech_scores = {
            "NN": 5,
            "VB": 2,
        }
        expected_search_scores = {
            "throw your banana and banana": 7
        }
        self.assertEqual(
            expected_search_scores,
            get_searches_scores(searches_containing_context_entities, parts_of_speech_scores)
        )

    def test_get_search_score_only_count_words_in_context_entities(self):
        searches_containing_context_entities = {
            "throw your banana": {
                "throw",
                "banana"
            }
        }
        parts_of_speech_scores = {
            "NN": 5,
            "VB": 2,
            "PRP$": 42
        }
        expected_search_scores = {
            "throw your banana": 7
        }
        self.assertEqual(
            expected_search_scores,
            get_searches_scores(searches_containing_context_entities, parts_of_speech_scores)
        )

    def test_get_searches_relative_scores(self):
        context_entities = {"throw", "banana"}
        search_scores = {
            "throw your banana": 4,
            "throw your apple": 2
        }
        parts_of_speech_scores = {
            "NN": 2,
            "VB": 2
        }
        expected_search_scores = {
            "throw your banana": 1,
            "throw your apple": 1/2
        }
        self.assertEqual(
            expected_search_scores,
            get_searches_relative_scores(context_entities, search_scores, parts_of_speech_scores)
        )
