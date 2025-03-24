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
            "grand_total_operations": {
                "terms": {
                    "field": "operation.keyword.terms.value",
                    "size": 30
                },
                "aggs": {
                    "amount": {
                        "sum": {
                            "field": "operation.keyword.terms._count"
                        }
                    }
                }
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
                    "total_operations": {
                        "terms": {
                            "field": "operation.keyword.terms.value",
                            "size": 20
                        },
                        "aggs": {
                            "amount": {
                                "sum": {
                                    "field": "operation.keyword.terms._count"
                                }
                            }
                        }
                    }
                }
            }
        }
