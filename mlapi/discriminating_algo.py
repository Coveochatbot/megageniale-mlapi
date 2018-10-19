import statistics

class DiscriminatingFacetsAlgo(object):
    def __init__(self):
        self.min_documents_per_facet = 3
        self.max_standard_deviation = 25
        self. min_values_per_facet = 2

    def get_discriminating_facets(self, facets_by_document):
        documents_by_facet = self.inverse_dictionary(facets_by_document)
        data = self.get_formated_data(documents_by_facet)
        result = self.execute_algorithm(data)
        if len(self.get_values_by_facet(result)) <= 1:
            self.adjust_parameters()
            data.clear()
            result.clear()
            data = self.get_formated_data(documents_by_facet)
            result = self.execute_algorithm(data)
        return self.get_values_by_facet(result)

    def inverse_dictionary(self, facets_by_document):
        documents_by_facet = {}
        for k, v in facets_by_document.items():
            for value in v:
                documents_by_facet[value] = documents_by_facet.get(value, [])
                documents_by_facet[value].append(k)
        return documents_by_facet

    def get_formated_data(self, documents_by_facet):
        data = {}
        unique_facets = []
        for facet, docs in documents_by_facet.items():
            one_facet = (facet.name, facet.value)
            if one_facet not in unique_facets:
                element = (facet.name, facet.value)
                data[element] = docs
                unique_facets.append(element)
            elif one_facet in unique_facets:
                data[element].append(docs)
        return data

    def get_facet_names(self, data):
        return list({facet[0] for facet in data.keys()})

    def get_values_by_facet(self,data):
        dict = {}
        unique_facets = []
        if data:
            for facet, docs in data.items():
                if facet[0] not in unique_facets:
                    dict[facet[0]] = [facet[1]]
                    unique_facets.append(facet[0])
                elif facet[0] in unique_facets:
                    dict[facet[0]].append(facet[1])
        return dict

    def get_facet_sample(self, data):
        facet_values_by_facet_name = self.get_values_by_facet(data)
        facet_names = self.get_facet_names(data)
        docs_count = 0
        dictionary = {}
        for index in range(len(facet_names)):
            for facet, docs in data.items():
                if facet[0] is facet_names[index]:
                    docs_count += len(docs)
            dictionary[facet_names[index]] = docs_count
            docs_count = 0

        for facet_name, nbr in dictionary.items():
            if (dictionary[facet_name] < self.min_documents_per_facet):
                for fn, fv in facet_values_by_facet_name.items():
                    if facet_name is fn:
                        for i in range(len(fv)):
                            one_facet = (fn, fv[i])
                            data.pop(one_facet)
        return data

    def get_uniformly_distributed_facets(self, data):
        docs_count_by_facet_value = {}
        standard_deviation = 50
        facet_names = self.get_facet_names(data)
        facet_values_by_facet_name = self.get_values_by_facet(data)
        for facet, docs in data.items():
            docs_count_by_facet_value[facet] = len(docs)
        for f_n in facet_names:
            counts = []
            for facet, nbr in docs_count_by_facet_value.items():
                if facet[0] == f_n:
                    counts.append(nbr)
            if len(counts)>= 2:
                standard_deviation = statistics.stdev(counts)
            if standard_deviation > self.max_standard_deviation:
                for facet_name, values in facet_values_by_facet_name.items():
                    if (facet_name == f_n):
                        for value in values:
                            one_facet = (f_n, value)
                            data.pop(one_facet)
        return data

    def get_facets_with_max_values(self, data):
        facet_values_by_facet_name = self.get_values_by_facet(data)
        facets_to_remove = []
        for facet_name, values in facet_values_by_facet_name.items():
            if len(values) < self.min_values_per_facet:
                for value in values:
                    one_facet = (facet_name, value)
                    facets_to_remove.append(one_facet)
        self.remove_entries(facets_to_remove, data)
        return data

    def remove_entries(self, list_of_tuples, data):
        for facet in list_of_tuples:
            data.pop(facet)

    def adjust_parameters(self):
        self.max_standard_deviation = self.max_standard_deviation + 10

    def execute_algorithm(self, data):
        facets_sample = self.get_facet_sample(data)
        uniformly_distributed_facets = self.get_uniformly_distributed_facets(facets_sample)
        return self.get_facets_with_max_values(uniformly_distributed_facets)