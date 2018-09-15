import json
from mlapi.model.facet import Facet


class FacetExtractor(object):

    @staticmethod
    def get_facets_from_file(files):
        return [FacetExtractor.extract_facet_from_file(file) for file in files]

    @staticmethod
    def extract_facet_from_file(file_path):
        with open(file_path) as jsonfile:
            data = json.load(jsonfile)
            name = data['FacetName']
            value = data['FacetValue']
            return Facet(name, value)
