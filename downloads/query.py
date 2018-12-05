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
    
    def _generate_data(self, filters, analysis_method):
        generated_query = QueryMaker().generate_query(filters, analysis_method)
        query_response = self.es.search(index=self.index,body=generated_query)
        if (analysis_method == "methods"):
            return self._generate_methods_data(filters, query_response)


    def _generate_methods_data(self, filters, response):
        json_data = {}
        json_data["title"] = "Summary of downloads from CEDA archive by method"
        json_data["filters"] = filters
        json_data["totals"] = {}
        json_data["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
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

class QueryMaker():
    def __init__(self):
        self._base_query = self._set__base_query()

    def generate_query(self, filters, analysis_method):
        self.generated_query = self._base_query
        self._update_filters(filters)
        self._update_aggs(analysis_method)
        return self.generated_query

    def _update_aggs(self, analysis_method):
        self.generated_query["aggs"].update(AggregationsMaker().get_aggs(analysis_method))
        
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

    def _set__base_query(self):
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
                "grand_total_method": {
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
                },
                "grand_total_activitydays": {
                    "sum_bucket": {
                        "buckets_path": "group_by>group_by_activitydays"
                    }
                }
            }
        }
