import unittest

from mlapi.analytics.get_suggested_documents_from_past_searches import get_parts_of_speech, \
    get_searches_containing_context_entities


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
        test_search = "throw your banana"
        expected_results = {
            "banana": "NN",
            "your": "PRP$",
            "throw": "VB"
        }
        self.assertEqual(get_parts_of_speech(test_search), expected_results)
