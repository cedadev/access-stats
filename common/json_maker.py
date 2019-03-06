from elasticsearch import Elasticsearch

from common.query_builder import QueryBuilder

class JsonMaker:
    def __init__(self, filters, analysis_method):
        self.filters = filters
        self.analysis_method = analysis_method
        
        self.user = self.get_credentials("access_stats/user.key")
        self.secret = self.get_credentials("access_stats/secret.key")
        self.host = "https://jasmin-es1.ceda.ac.uk"
        self.index = "logstash-test"
        
        self.es = Elasticsearch(
            [self.host],
            http_auth=(self.user,self.secret),
            timeout=30
        )

    def get_credentials(self, file_name):
        with open(file_name) as secrets:
            return secrets.read()

    def get_elasticsearch_response(self):
        query = QueryBuilder(self.filters, self.analysis_method).query()
        return self.es.search(index = self.index, body = query)

    def get_title(self):
        return NotImplementedError

    def _populate_json(self, json):
        return NotImplementedError

    def json(self):
        json = {}
        json["title"] = self.get_title()
        json["filters"] = self.filters
        self._populate_json(json)

        return json
