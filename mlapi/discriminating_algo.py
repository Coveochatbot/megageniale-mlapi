import statistics

class DiscriminatingFacetsAlgo(object):
    facets_sample_count = 3  # minimum docs by facet to be accepted
    tolerance_interval = 25 # max standard deviation accepted ()
    nbr_facet_values = 2 # to consider a facet as having a large number of values

    result = {}

    def get_discriminating_facets_algo(self, facets_by_document):
        documents_by_facet = self.inverse_dictionary(facets_by_document)
        data = self.get_formated_data(documents_by_facet)
        self.execute_algorithm(data)
        if len(self.get_values_by_facet(self.result)) <= 1:
            self.adjust_parameters()
            data.clear()
            data = self.get_formated_data(documents_by_facet)
            self.execute_algorithm(data)
        return self.get_values_by_facet(self.result)

    def inverse_dictionary(self, facets_by_document):
        documents_by_facet = {}
        for k, v in facets_by_document.items():
            for value in v:
                documents_by_facet[value] = documents_by_facet.get(value, [])
                documents_by_facet[value].append(k)
        return documents_by_facet

    def get_formated_data(self, documents_by_facet):
        data = {}
        list = []
        for facet, docs in documents_by_facet.items():
            t = (facet.name, facet.value)
            if t not in list:
                tuple = (facet.name, facet.value)
                data[tuple] = docs
                list.append(tuple)
            elif t in list:
                data[tuple].append(docs)
        return data

    def get_facet_names(self, data):
        list = []
        for facet, docs in data.items():
            if facet[0] not in list:
                list.append(facet[0])
        return list

    def get_values_by_facet(self,data):
        dict = {}
        list = []
        if data:
            for facet, docs in data.items():
                if facet[0] not in list:
                    dict[facet[0]] = [facet[1]]
                    list.append(facet[0])
                elif facet[0] in list:
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
            if (dictionary[facet_name] < self.facets_sample_count): # 1st filter
                for fn, fv in facet_values_by_facet_name.items():
                    if facet_name is fn:
                        for i in range(len(fv)):
                            t = (fn, fv[i])
                            result = data.pop(t)
        return data

    def get_equitably_distributed_facets(self, data):
        docs_count_by_facet_value = {}
        standard_deviation = 50
        facet_names = self.get_facet_names(data)
        facet_values_by_facet_name = self.get_values_by_facet(data)
        for facet, docs in data.items():
            docs_count_by_facet_value[facet] = len(docs)
        for f in facet_names:
            list = []
            for facet, nbr in docs_count_by_facet_value.items():
                if facet[0] == f:
                    list.append(nbr)
            if len(list)>= 2:
                standard_deviation = statistics.stdev(list)
            if standard_deviation > self.tolerance_interval: # 2nd filter
                for facet_name, values in facet_values_by_facet_name.items():
                    if (facet_name == f):
                        for value in values:
                            t = (f, value)
                            data.pop(t)
        return data

    def get_facets_with_max_values(self, data):
        facet_values_by_facet_name = self.get_values_by_facet(data)
        facets_to_remove = []
        for facet_name, values in facet_values_by_facet_name.items():
            if not (len(values) > self.nbr_facet_values): # 3rd filter
                for value in values:
                    t = (facet_name, value)
                    facets_to_remove.append(t)
        self.remove_entries(facets_to_remove, data)
        return data

    def remove_entries(self, list_of_tuples, data):
        for t in list_of_tuples:
            data.pop(t)

    def adjust_parameters(self):
        self.tolerance_interval = self.tolerance_interval + 10

    def execute_algorithm(self, data):
        facets_sample = self.get_facet_sample(data)
        equitably_distributed_facets = self.get_equitably_distributed_facets(facets_sample)
        self.result = self.get_facets_with_max_values(equitably_distributed_facets)