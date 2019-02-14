import datetime
from elasticsearch import Elasticsearch

from .query import QueryMaker

class QueryElasticSearch:
    def __init__(self):
        self.secret = self.get_credentials("downloads/secret.key")
        self.user = self.get_credentials("downloads/user.key")
        self.host = "https://jasmin-es-test.ceda.ac.uk"
        self.index = "logstash-test"
        self.es = Elasticsearch(
            [self.host],
            http_auth=(self.user,self.secret),
            timeout=30
        )

    def get_credentials(self, file_name):
        with open(file_name) as secrets:
            return secrets.read()
            
    def get_data(self, filters, analysis_method):
        return self._generate_data(filters, analysis_method)

    def get_query_response(self, body):
        return self.es.search(index=self.index,body=body)
    
    def _generate_data(self, filters, analysis_method):
        # Generates a query with the QueryMaker class
        generated_query = QueryMaker().generate_query(filters, analysis_method)
        # Uses this query to get data back from ES
        query_response = self.get_query_response(body=generated_query)
        # Formats data dependent on analysis_method
        if analysis_method == "methods":
            return self._generate_methods_data(filters, query_response)
        if analysis_method == "timeline":
            return self._generate_timeline_data(filters, query_response)
        if analysis_method == "dataset":
            return self._generate_dataset_data(filters, query_response)
        if analysis_method == "dataset-limited":
            return self._generate_dataset_limited_data(filters, query_response)
        if analysis_method == "user":
            return self._generate_user_data(filters, query_response)
        if analysis_method == "users":
            return self._generate_users_data(filters, query_response)
        if analysis_method == "users-limited":
            return self._generate_users_limited_data(filters, query_response)
        if analysis_method == "trace":
            return self._generate_trace_data(filters, query_response)

    def _generate_methods_data(self, filters, response):
        json_data = {}
        json_data["title"] = "Summary of downloads from CEDA archive by method"
        json_data["filters"] = filters
        json_data["totals"] = {}
        json_data["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        json_data["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        json_data["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        json_data["totals"]["accesses"] = response["hits"]["total"]
        json_data["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        json_data["totals"]["activitydays"] = response["aggregations"]["grand_total_activitydays"]["value"]

        json_data["results"] = {}
        for result in response["aggregations"]["group_by"]["buckets"]:
            json_data["results"][result["key"]] = {}
            json_data["results"][result["key"]]["users"] = result["number_of_users"]["value"]
            json_data["results"][result["key"]]["datasets"] = result["number_of_datasets"]["value"]
            json_data["results"][result["key"]]["accesses"] = result["doc_count"]
            json_data["results"][result["key"]]["size"] = result["total_size"]["value"]
            json_data["results"][result["key"]]["activitydays"] = result["group_by_activitydays"]["value"]

        return json_data

    def _generate_timeline_data(self, filters, response):
        json_data = {}
        json_data["title"] = "Timeline for downloads from CEDA archive"
        json_data["filters"] = filters
        json_data["totals"] = {}
        json_data["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        json_data["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        json_data["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        json_data["totals"]["accesses"] = response["hits"]["total"]
        json_data["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        json_data["totals"]["activitydays"] = response["aggregations"]["grand_total_activitydays"]["value"]

        json_data["results"] = {}
        for result in response["aggregations"]["group_by"]["buckets"]:
            month = result["key_as_string"]
            json_data["results"][month] = {}
            json_data["results"][month]["users"] = result["number_of_users"]["value"]
            json_data["results"][month]["methods"] = result["number_of_methods"]["value"]
            json_data["results"][month]["datasets"] = result["number_of_datasets"]["value"]
            json_data["results"][month]["accesses"] = result["doc_count"]
            json_data["results"][month]["size"] = result["total_size"]["value"]
            json_data["results"][month]["activitydays"] = result["group_by_activitydays"]["value"]

        return json_data

    def _generate_dataset_data(self, filters, response):
        json_data = {}
        json_data["title"] = "Summary of downloads from CEDA archive by dataset"
        json_data["filters"] = filters
        json_data["totals"] = {}
        json_data["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        json_data["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        json_data["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        json_data["totals"]["accesses"] = response["hits"]["total"]
        json_data["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        json_data["totals"]["activitydays"] = 0

        json_data["results"] = {}
        while response["aggregations"]["group_by"]["buckets"] != []:
            for result in response["aggregations"]["group_by"]["buckets"]:
                json_data["results"][result["key"]["dataset"]] = {}
                json_data["results"][result["key"]["dataset"]]["users"] = result["number_of_users"]["value"]
                json_data["results"][result["key"]["dataset"]]["methods"] = result["number_of_methods"]["value"]
                json_data["results"][result["key"]["dataset"]]["accesses"] = result["doc_count"]
                json_data["results"][result["key"]["dataset"]]["size"] = result["total_size"]["value"]
                json_data["results"][result["key"]["dataset"]]["activitydays"] = result["group_by_activitydays"]["value"]
                json_data["totals"]["activitydays"] += result["group_by_activitydays"]["value"]

            after_key = response["aggregations"]["group_by"]["after_key"]
            generated_query = QueryMaker().generate_query(filters, "dataset", after_key)
            response = self.get_query_response(body=generated_query)
            
        return json_data
    
    def _generate_dataset_limited_data(self, filters, response):
        json_data = {}
        json_data["title"] = "Summary of downloads from CEDA archive by dataset"
        json_data["filters"] = filters
        json_data["totals"] = {}
        json_data["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        json_data["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        json_data["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        json_data["totals"]["accesses"] = response["hits"]["total"]
        json_data["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        json_data["totals"]["activitydays"] = response["aggregations"]["grand_total_activitydays"]["value"]

        json_data["results"] = {}
        for result in response["aggregations"]["group_by"]["buckets"]:
            json_data["results"][result["key"]] = {}
            json_data["results"][result["key"]]["users"] = result["number_of_users"]["value"]
            json_data["results"][result["key"]]["methods"] = result["number_of_methods"]["value"]
            json_data["results"][result["key"]]["accesses"] = result["doc_count"]
            json_data["results"][result["key"]]["size"] = result["total_size"]["value"]
            json_data["results"][result["key"]]["activitydays"] = result["group_by_activitydays"]["value"]

        return json_data

    def _generate_user_data(self, filters, response):
        json_data = {}
        json_data["title"] = "User breakdown of downloads from CEDA archive"
        json_data["filters"] = filters

        json_data["results"] = {}
        for grouping in response["aggregations"]:
            json_data["results"][grouping] = {}
            for result in response["aggregations"][grouping]["buckets"]:
                json_data["results"][grouping][result["key"]] = result["users"]["value"]

        return json_data

    def _generate_users_data(self, filters, response):
        json_data = {}
        json_data["title"] = "Summary of downloads from CEDA archive by user"
        json_data["filters"] = filters
        json_data["totals"] = {}
        json_data["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        json_data["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        json_data["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        json_data["totals"]["accesses"] = response["hits"]["total"]
        json_data["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        json_data["totals"]["activitydays"] = 0

        json_data["results"] = {}
        while response["aggregations"]["group_by"]["buckets"] != []:
            for result in response["aggregations"]["group_by"]["buckets"]:
                json_data["results"][result["key"]["user"]] = {}
                if result["key"]["user"].startswith("anonymous@"):
                    json_data["results"][result["key"]["user"]]["country"] = result["country"]["buckets"][0]["key"]
                    json_data["results"][result["key"]["user"]]["institute_type"] = "-"
                    json_data["results"][result["key"]["user"]]["field"] = "-"
                else:
                    json_data["results"][result["key"]["user"]]["country"] = result["country"]["buckets"][0]["key"]
                    json_data["results"][result["key"]["user"]]["institute_type"] = result["institute_type"]["buckets"][0]["key"]
                    json_data["results"][result["key"]["user"]]["field"] = result["field"]["buckets"][0]["key"]
                json_data["results"][result["key"]["user"]]["methods"] = result["number_of_methods"]["value"]
                json_data["results"][result["key"]["user"]]["datasets"] = result["number_of_datasets"]["value"]
                json_data["results"][result["key"]["user"]]["accesses"] = result["doc_count"]
                json_data["results"][result["key"]["user"]]["size"] = result["total_size"]["value"]
                json_data["results"][result["key"]["user"]]["activitydays"] = result["group_by_activitydays"]["value"]
                json_data["totals"]["activitydays"] += result["group_by_activitydays"]["value"]
            after_key = response["aggregations"]["group_by"]["after_key"]
            generated_query = QueryMaker().generate_query(filters, "users", after_key)
            response = self.get_query_response(body=generated_query)
            
        return json_data
    

    def _generate_users_limited_data(self, filters, response):
        json_data = {}
        json_data["title"] = "Summary of downloads from CEDA archive by user"
        json_data["filters"] = filters
        json_data["totals"] = {}
        json_data["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        json_data["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        json_data["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        json_data["totals"]["accesses"] = response["hits"]["total"]
        json_data["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        json_data["totals"]["activitydays"] = response["aggregations"]["grand_total_activitydays"]["value"]

        json_data["results"] = {}
        for result in response["aggregations"]["group_by"]["buckets"]:
            json_data["results"][result["key"]] = {}
            if result["key"].startswith("anonymous@"):
                json_data["results"][result["key"]]["country"] = result["country"]["buckets"][0]["key"]
                json_data["results"][result["key"]]["institute_type"] = "-"
                json_data["results"][result["key"]]["field"] = "-"
            else:
                json_data["results"][result["key"]]["country"] = result["country"]["buckets"][0]["key"]
                json_data["results"][result["key"]]["institute_type"] = result["institute_type"]["buckets"][0]["key"]
                json_data["results"][result["key"]]["field"] = result["field"]["buckets"][0]["key"]
            json_data["results"][result["key"]]["methods"] = result["number_of_methods"]["value"]
            json_data["results"][result["key"]]["datasets"] = result["number_of_datasets"]["value"]
            json_data["results"][result["key"]]["accesses"] = result["doc_count"]
            json_data["results"][result["key"]]["size"] = result["total_size"]["value"]
            json_data["results"][result["key"]]["activitydays"] = result["group_by_activitydays"]["value"]

        return json_data

    def _generate_trace_data(self, filters, response):
        json_data = {}
        json_data["title"] = "List of logs within filter"
        json_data["filters"] = filters
        json_data["logs"] = []
        for result in response["hits"]["hits"]:
            try:
               json_data["logs"].append(f'{result["_source"]["datetime"]},{result["_source"]["method"]},{result["_source"]["filename"]},{result["_source"]["size"]},{result["_source"]["user"]},{result["_source"]["ip"]},{result["_source"]["dataset"]}')
            except KeyError:
                continue
        
        return json_data