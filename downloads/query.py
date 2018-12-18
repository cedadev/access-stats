import datetime
from elasticsearch import Elasticsearch

from .aggregations import AggregationsMaker

class QueryElasticSearch:
    def __init__(self):
        self.host = "jasmin-es-test.ceda.ac.uk"
        self.index = "tommy-test"
        self.port = 9200
        self.es = Elasticsearch(hosts=[{"host": self.host, "port": self.port}])
        
    def get_data(self, filters, analysis_method):
        return self._generate_data(filters, analysis_method)

    def get_query_response(self, body):
        return self.es.search(index=self.index,body=body)
    
    def _generate_data(self, filters, analysis_method):
        if analysis_method == "user":
            return {}
        generated_query = QueryMaker().generate_query(filters, analysis_method)
        query_response = self.get_query_response(body=generated_query)
        if analysis_method == "methods":
            return self._generate_methods_data(filters, query_response)
        if analysis_method == "timeline":
            return self._generate_timeline_data(filters, query_response)
        if analysis_method == "dataset":
            return self._generate_dataset_data(filters, query_response)
        if analysis_method == "users":
            return self._generate_users_data(filters, query_response)
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
            month = datetime.datetime.strptime(result["key_as_string"],"%Y/%m/%d-%H:%M:%S").strftime("%Y/%m/%d")
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

    def _generate_trace_data(self, filters, response):
        json_data = {}
        json_data["title"] = "List of logs within filter"
        json_data["filters"] = filters
        json_data["logs"] = []
        for result in response["hits"]["hits"]:
            json_data["logs"].append(f'{result["_source"]["datetime"]},{result["_source"]["method"]},{result["_source"]["filename"]},{result["_source"]["size"]},{result["_source"]["user"]},{result["_source"]["ip"]},{result["_source"]["dataset"]}')
        
        return json_data

class QueryMaker():
    def generate_query(self, filters, analysis_method, after_key=None):
        if analysis_method == "trace":
            self.generated_query = self._base_small_query()
        else:
            self.generated_query = self._base_big_query()
        self._update_filters(filters)
        if analysis_method != "trace":
            self._update_aggs(analysis_method, after_key)
        return self.generated_query

    def _update_aggs(self, analysis_method, after_key):
        if analysis_method != "users" and analysis_method != "dataset":
            self.generated_query["aggs"].update(self.total_activitydays())
        self.generated_query["aggs"].update(AggregationsMaker().get_aggs(analysis_method, after_key))
        
    def _update_filters(self, filters):
        if filters["start"]:
            self.generated_query["query"]["bool"]["filter"]["range"]["datetime"]["gte"] = filters["start"]
        if filters["end"]:
            self.generated_query["query"]["bool"]["filter"]["range"]["datetime"]["lte"] = filters["end"]
        if filters["user"]:
            self.generated_query["query"]["bool"]["must"].append({
                        "match_phrase": {
                            "user": filters["user"]
                        }
                    })
        if filters["dataset"]:
            self.generated_query["query"]["bool"]["must"].append({
                        "match_phrase_prefix": {
                            "dataset": filters["dataset"]
                        }
                    })
        if filters["method"]:
            self.generated_query["query"]["bool"]["must"].append({
                        "match_phrase": {
                            "method": filters["method"]
                        }
                    })
        if filters["anon"]:
            if filters["anon"] == "anon":
                self.generated_query["query"]["bool"]["must"].append({
                            "match_phrase_prefix": {
                                "user": "anonymous@"
                            }
                        })
            if filters["anon"] == "non-anon":
                self.generated_query["query"]["bool"]["must_not"].append({
                            "match_phrase_prefix": {
                                "user": "anonymous@"
                            }
                        })

    def total_activitydays(self):
        return {"grand_total_activitydays": {
            "sum_bucket": {
                "buckets_path": "group_by>group_by_activitydays"
            }
        }
        }

    def _base_small_query(self):
        return {
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [],
                    "should": [],
                    "filter": {
                        "range": {
                            "datetime": {
                                "gte": "2012-01-01",
                                "lte": "now",
                                "format": "yyyy-MM-dd"
                            }
                        }
                    }
                }
            },
            "_source": [],
            "size": 1000
        }

    def _base_big_query(self):
        return {
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [],
                    "should": [],
                    "filter": {
                        "range": {
                            "datetime": {
                                "gte": "2012-01-01",
                                "lte": "now",
                                "format": "yyyy-MM-dd"
                            }
                        }
                    }
                }
            },
            "_source": [],
            "size": 0,
            "sort": [],
            "aggs": {
                "grand_total_users": {
                    "cardinality": {
                        "field": "user.keyword"
                    }
                },
                "grand_total_methods": {
                    "cardinality": {
                        "field": "method.keyword"
                    }
                },
                "grand_total_datasets": {
                    "cardinality": {
                        "field": "dataset.keyword"
                    }
                },
                "grand_total_size": {
                    "sum": {
                        "field": "size"
                    }
                }
            }
        }
