from collections import defaultdict

import nltk

nltk.download('averaged_perceptron_tagger')


def get_searches_containing_context_entities(searches_documents_mapping, context_entities):
    searches_containing_context_entities = defaultdict(set)
    for search_document_mapping in searches_documents_mapping:
        for context_entity in context_entities:
            if context_entity in search_document_mapping.split():
                searches_containing_context_entities[search_document_mapping].add(context_entity)
    return searches_containing_context_entities


def get_words_and_parts_of_speech(speech):
    return {word: part_of_speech for (word, part_of_speech) in nltk.pos_tag(speech)}


def get_searches_scores(searches_containing_context_entities, parts_of_speech_scores):
    searches_scores = defaultdict(int)
    for search, contained_context_entities in searches_containing_context_entities.items():
        words_and_parts_of_speech = get_words_and_parts_of_speech(search.split())
        score = 0
        for word, part_of_speech in words_and_parts_of_speech.items():
            if word in contained_context_entities:
                score += parts_of_speech_scores[part_of_speech] if part_of_speech in parts_of_speech_scores else 0
        searches_scores[search] = score
    return searches_scores


def get_searches_relative_scores(context_entities, search_scores, parts_of_speech_scores):
    context_entities_string = " ".join(context_entities)
    max_score = get_searches_scores(
        {context_entities_string: context_entities},
        parts_of_speech_scores
    )[context_entities_string]
    return {search: search_scores[search] / max_score for search in search_scores.keys()}
