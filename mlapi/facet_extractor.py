import json
from mlapi.model.facet import Facet


class FacetExtractor(object):

    def get_facets_by_document(self, files):
        dictionary = {}
        for file in files:
            facet, documents = FacetExtractor.extract_facet_from_file(file)
            dictionary[facet] = documents
        return self.invert_dictionary(dictionary)

    @staticmethod
    def invert_dictionary(dictionary):
        inv_map = {}
        for k, v in dictionary.items():
            for value in v:
                inv_map[value] = inv_map.get(value, [])
                inv_map[value].append(k)
        return inv_map

    @staticmethod
    def extract_facet_from_file(file_path):
        with open(file_path) as jsonfile:
            data = json.load(jsonfile)
            name = data['FacetName']
            value = data['FacetValue']
            documents = []
            for document in data['Documents']:
                documents.append(document['ClickUri'])
            return Facet(name, value), documents
