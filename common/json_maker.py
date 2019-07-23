import yaml
from pathlib import Path

from elasticsearch import Elasticsearch

from common.query_builder_factory import QueryBuilderFactory

class JsonMaker:
    def __init__(self, filters, analysis_method):
        self.filters = filters
        self.analysis_method = analysis_method

        parent_dir = (Path(__file__).parent).parent
        settings_file = parent_dir.joinpath("access_stats/settings.yml")
        if not settings_file.exists():
            raise FileNotFoundError(f"{settings_file} not found")

        self.load_settings(settings_file)
        
        self.es = Elasticsearch(
            [self.settings["host"]],
            http_auth=(self.settings["user"], self.settings["password"]),
            timeout=60
        )
    
    def index(self):
        return "rollup"

    def load_settings(self, file_name):
        with open(file_name) as secrets:
            try:
                self.settings = yaml.safe_load(secrets)
            except yaml.YAMLError as e:
                raise RuntimeError(f"settings.yml file incorrect yaml: {e}")

    def get_elasticsearch_response(self, after_key = None, deposits = False):
        query = QueryBuilderFactory(deposits = deposits).get(self.filters, self.analysis_method, after_key).query()
        index = self.settings["index"][self.index()]

        return self.es.search(index = index, body = query)

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
