from elasticsearch import Elasticsearch

class QueryElasticSearch:
    def __init__(self):
        self.host = "jasmin-es-test.ceda.ac.uk"
        self.index = "tommy-test"
        self.port = 9200
        self.es = Elasticsearch(hosts=[{"host": self.host, "port": self.port}])
        
    def get_data(self, filters, analysis_method):
        if analysis_method == "methods":
            return self._generate_methods_data(filters)
    
    def _generate_methods_data(self, filters):
        req = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "dataset": "/badc"
                            }
                        }
                    ],
                    "must_not": [],
                    "should": [],
                    "filter": {
                        "range": {
                            "datetime": {
                                "gte": "2018/01/01-00:00:00",
                                "lte": "2018/11/26-00:00:00",
                                "format": "yyyy/MM/dd-HH:mm:ss"

                            }
                        }
                    }
                }
            },
            "_source": [],
            "size": 0,
            "sort": [],
            "aggs": {
                "group_by_method": {
                    "terms": {
                        "field": "method.keyword"
                    },
                    "aggs": {
                        "number_of_users": {
                            "cardinality": {
                                "field": "user.keyword"
                            }
                        },
                        "number_of_datasets": {
                            "cardinality": {
                                "field": "dataset.keyword"
                            }
                        },
                        "total_size": {
                            "sum": {
                                "field": "size"
                            }
                        }
                    }
                }
            }
        }

        return self.es.search(index=self.index,body=req)
