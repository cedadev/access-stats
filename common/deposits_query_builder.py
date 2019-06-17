from common.query_builder import QueryBuilder


class DepositsQueryBuilder(QueryBuilder):
    def operation(self):
        return "operation.keyword.terms.value"

    def base_query(self):
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                self.method(): "deposits"
                            }
                        }
                    ],
                    "must_not": [],
                    "should": [],
                    "filter": {
                        "range": {
                            self.datetime(): {
                                "gte": "2012-01-01",
                                "lte": "now",
                                "format": "yyyy-MM-dd"
                            }
                        }
                    }
                }
            },
            "_source": [],
            "size": self.get_size(),
            "aggs": {}
        }

    def update_filters(self):
        if self.filters["start"]:
            self.generated_query["query"]["bool"]["filter"]["range"][self.datetime()]["gte"] = self.filters["start"]
        if self.filters["end"]:
            self.generated_query["query"]["bool"]["filter"]["range"][self.datetime()]["lte"] = self.filters["end"]
        if self.filters["dataset"]:
            self.generated_query["query"]["bool"]["must"].append({
                        "wildcard": {
                            self.dataset(): {
                                "value": f'*{self.filters["dataset"]}*'
                            }
                        }
                    })

    def grand_totals(self):
        self.generated_query["aggs"].update({
            "grand_total_size": {
                "sum": {
                    "field": self.size()
                }
            },
            "grand_total_datasets": {
                "cardinality": {
                    "field": self.dataset()
                }
            },
            "grand_total_deposits": {
                "filter": { "term": { self.operation(): "DEPOSIT" }}
            },
            "grand_total_mkdir": {
                "filter": { "term": { self.operation(): "MKDIR" }}
            },
            "grand_total_symlink": {
                "filter": { "term": { self.operation(): "SYMLINK" }}
            },
            "grand_total_rmdir": {
                "filter": { "term": { self.operation(): "RMDIR" }}
            },
            "grand_total_remove": {
                "filter": { "term": { self.operation(): "REMOVE" }}
            }
        })

    def base_aggs(self):
        return {
            "group_by": {
                "aggs": {
                    "total_size": {
                        "sum": {
                            "field": self.size()
                        }
                    },
                    "number_of_datasets": {
                        "cardinality": {
                            "field": self.dataset()
                        }
                    },
                    "number_of_deposits": {
                        "filter": { "term": { self.operation(): "DEPOSIT" }}
                    },
                    "number_of_mkdir": {
                        "filter": { "term": { self.operation(): "MKDIR" }}
                    },
                    "number_of_symlink": {
                        "filter": { "term": { self.operation(): "SYMLINK" }}
                    },
                    "number_of_rmdir": {
                        "filter": { "term": { self.operation(): "RMDIR" }}
                    },
                    "number_of_remove": {
                        "filter": { "term": { self.operation(): "REMOVE" }}
                    }
                }
            }
        }
