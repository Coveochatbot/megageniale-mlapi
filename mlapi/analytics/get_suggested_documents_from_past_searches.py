from collections import defaultdict

import nltk


def get_searches_containing_context_entities(searches_documents_mapping, context_entities):
    searches_containing_context_entities = defaultdict(set)
    for search_document_mapping in searches_documents_mapping:
        for context_entity in context_entities:
            if context_entity in search_document_mapping.split():
                searches_containing_context_entities[search_document_mapping].add(context_entity)
    return searches_containing_context_entities


def get_parts_of_speech(speech):
    words = nltk.tokenize.word_tokenize(speech)
    parts_of_speech = nltk.pos_tag(words)
    parts_of_speech_dict = defaultdict(set)
    for part in parts_of_speech:
        parts_of_speech_dict[part[0]] = part[1]
    return parts_of_speech_dict


