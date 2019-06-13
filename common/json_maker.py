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

    def load_settings(self, file_name):
        with open(file_name) as secrets:
            try:
                self.settings = yaml.safe_load(secrets)
            except yaml.YAMLError as e:
                raise RuntimeError(f"settings.yml file incorrect yaml: {e}")

    def get_elasticsearch_response(self, after_key = None, deposits = False, activity_days = False):
        query = QueryBuilderFactory(deposits = deposits).get(self.filters, self.analysis_method, after_key).query(activity_days)
        if activity_days:
            index = self.settings["index"]["activity_days"]
        else:
            index = self.settings["index"]["main"]

        return self.es.search(index = index, body = query)

    def get_activity_days(self, response, identifier):
        buckets = response["aggregations"]["group_by"]["buckets"]
        for bucket in buckets:
            if bucket["key"] == identifier:
                return bucket["doc_count"]

    def get_activity_days_dict(self, field):
        activity_days_dict = {}
        response = self.get_elasticsearch_response(after_key=0, activity_days=True)
        while response["aggregations"]["group_by"]["buckets"] != []:
            for bucket in response["aggregations"]["group_by"]["buckets"]:
                activity_days_dict[bucket["key"][field]] = bucket["doc_count"]
            after_key = response["aggregations"]["group_by"]["after_key"]
            response = self.get_elasticsearch_response(after_key = after_key, activity_days=True)
        return activity_days_dict

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
