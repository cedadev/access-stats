import yaml
from elasticsearch import Elasticsearch

from common.query_builder_factory import QueryBuilderFactory

class JsonMaker:
    def __init__(self, filters, analysis_method):
        self.filters = filters
        self.analysis_method = analysis_method

        self.load_settings("access_stats/settings.yml")
    
        self.host = "https://jasmin-es1.ceda.ac.uk"
        
        self.es = Elasticsearch(
            [self.host],
            http_auth=(self.settings["user"], self.settings["password"]),
            timeout=30
        )

    def load_settings(self, file_name):
        with open(file_name) as secrets:
            try:
                self.settings = yaml.safe_load(secrets)
            except yaml.YAMLError as e:
                print(e)

    def get_elasticsearch_response(self, after_key = None, deposits = False):
        query = QueryBuilderFactory(deposits=deposits).get(self.filters, self.analysis_method, after_key).query()
        return self.es.search(index = self.settings["index"], body = query)

    def get_title(self):
        return NotImplementedError

    def _populate_json(self):
        return NotImplementedError

    def generate_json(self):
        self.generated_json = {}
        self.generated_json["title"] = self.get_title()
        self.generated_json["filters"] = self.filters
        self._populate_json()

    def json(self):
        self.generate_json()
        return self.generated_json
