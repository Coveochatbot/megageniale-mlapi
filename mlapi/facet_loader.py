import json
from mlapi.serialization.object_decoder import ObjectDecoder
from mlapi.serialization.object_encoder import ObjectEncoder


class FacetLoader(object):
    def load_facets(self, facet_file):
        file = open(facet_file, "rb")
        facets = self.binary_to_dict(file.read())
        file.close()
        return facets

    def save_facets(self, facet_dictionary, save_path):
        binary_data = self.dict_to_binary(facet_dictionary)
        file = open(save_path, 'wb')
        file.write(binary_data)
        file.close()

    @staticmethod
    def dict_to_binary(dictionary):
        return json.dumps(dictionary, cls=ObjectEncoder).encode('utf-8')

    @staticmethod
    def binary_to_dict(binary_data):
        return json.loads(binary_data.decode('utf-8'), cls=ObjectDecoder)
