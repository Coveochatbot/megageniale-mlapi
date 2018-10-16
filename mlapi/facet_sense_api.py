import requests
from requests.auth import HTTPBasicAuth
from definitions import Definitions
from pathlib import Path
import json


class FacetSenseApi(object):
    API_URL = "https://whispersherbrooke2018.cloud.coveo.com/predict"
    QUERY = "{{\"q\": \"{text}\"}}"
    CREDENTIALS_PATH = Path(Definitions.ROOT_DIR + "/appsettings.json")

    def __init__(self):
        file = open(FacetSenseApi.CREDENTIALS_PATH, 'r')
        values = json.load(file)
        self.username = values['facetSenseUsername']
        self.password = values['facetSensePassword']
        file.close()

    def get_facet_scores(self, text):
        query = FacetSenseApi.QUERY.format(text=text)
        response = requests.post(FacetSenseApi.API_URL, data=query, auth=HTTPBasicAuth(self.username, self.password))
        return response.content
