from collections import defaultdict

import nltk
import operator

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


def get_suggested_documents(
        suggested_documents_limit,
        searches_relative_scores,
        documents_popularity_mapping,
        searches_documents_mapping,
        relative_scores_threshold):
    searches_relative_scores_over_threshold = {
        search: relative_score
        for search, relative_score in searches_relative_scores.items()
        if relative_score > relative_scores_threshold
    }
    documents_relatives_scores = defaultdict(float)
    for search, documents in searches_documents_mapping.items():
        if search not in searches_relative_scores_over_threshold:
            continue
        for document in documents:
            if document in documents_relatives_scores and documents_relatives_scores[document] < searches_relative_scores[search]:
                documents_relatives_scores[document] = searches_relative_scores[search]
            if document not in documents_relatives_scores:
                documents_relatives_scores[document] = searches_relative_scores[search]
    documents_scores = {
        document: relative_score * documents_popularity_mapping[document]
        for document, relative_score in documents_relatives_scores.items()
        if document in documents_popularity_mapping
    }
    suggested_documents_scores = sorted(documents_scores.items(), key=operator.itemgetter(1), reverse=True)[:suggested_documents_limit]
    return [suggested_document_score[0] for suggested_document_score in suggested_documents_scores]