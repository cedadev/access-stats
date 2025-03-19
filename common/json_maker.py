import yaml
from pathlib import Path

from elasticsearch import Elasticsearch

from common.query_builder_factory import QueryBuilderFactory


class JsonMaker:

    INDEX_KEY = "rollup"

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
            headers={"x-api-key": self.settings["es_api_key"]},
            ca_certs=None,
            timeout=60,
        )

    @property
    def index(self):
        return self.settings["index"][self.INDEX_KEY]

    def load_settings(self, file_name):
        with open(file_name) as secrets:
            try:
                self.settings = yaml.safe_load(secrets)
            except yaml.YAMLError as e:
                raise RuntimeError(f"settings.yml file incorrect yaml: {e}")

    def get_activity_days(self, total_response):
        """
        Returns total number of activity days. Handles getting the total number, even if the number is > 10k
        :param total_response: The total object from the elasticsearch JSON response
        :return: <int> Total number of activity days
        """

        if total_response["relation"] == "eq":
            return total_response["value"]
        else:
            query = self.get_elasticsearch_query()
            query.pop("_source", None)
            query.pop("aggs", None)
            query.pop("size", None)
            return self.es.count(index=self.index, body=query)["count"]

    def get_elasticsearch_response(self, after_key=None, deposits=False):
        query = self.get_elasticsearch_query(after_key, deposits)
        return self.es.search(index=self.index, body=query)

    def get_elasticsearch_query(self, after_key=None, deposits=False):
        return (
            QueryBuilderFactory(deposits=deposits)
            .get(self.filters, self.analysis_method, after_key)
            .query()
        )

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
