from common.query_builder import QueryBuilder


class DepositsQueryBuilder(QueryBuilder):
    def base_query(self):
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "method": "deposits"
                            }
                        }
                    ],
                    "must_not": [],
                    "should": [],
                    "filter": {
                        "range": {
                            self.get_date_unit(): {
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
            self.generated_query["query"]["bool"]["filter"]["range"]["datetime"]["gte"] = self.filters["start"]
        if self.filters["end"]:
            self.generated_query["query"]["bool"]["filter"]["range"]["datetime"]["lte"] = self.filters["end"]
        if self.filters["dataset"]:
            self.generated_query["query"]["bool"]["must"].append({
                        "match_phrase_prefix": {
                            "dataset": self.filters["dataset"]
                        }
                    })

    def grand_totals(self):
        self.generated_query["aggs"].update({
            "grand_total_size": {
                "sum": {
                    "field": "size"
                }
            },
            "grand_total_datasets": {
                "cardinality": {
                    "field": "dataset.keyword"
                }
            },
            "grand_total_deposits": {
                "filter": { "term": { "operation.keyword": "DEPOSIT" }}
            },
            "grand_total_mkdir": {
                "filter": { "term": { "operation.keyword": "MKDIR" }}
            },
            "grand_total_symlink": {
                "filter": { "term": { "operation.keyword": "SYMLINK" }}
            },
            "grand_total_rmdir": {
                "filter": { "term": { "operation.keyword": "RMDIR" }}
            },
            "grand_total_remove": {
                "filter": { "term": { "operation.keyword": "REMOVE" }}
            }
        })

    def base_aggs(self):
        return {
            "group_by": {
                "aggs": {
                    "total_size": {
                        "sum": {
                            "field": "size"
                        }
                    },
                    "number_of_datasets": {
                        "cardinality": {
                            "field": "dataset.keyword"
                        }
                    },
                    "number_of_deposits": {
                        "filter": { "term": { "operation.keyword": "DEPOSIT" }}
                    },
                    "number_of_mkdir": {
                        "filter": { "term": { "operation.keyword": "MKDIR" }}
                    },
                    "number_of_symlink": {
                        "filter": { "term": { "operation.keyword": "SYMLINK" }}
                    },
                    "number_of_rmdir": {
                        "filter": { "term": { "operation.keyword": "RMDIR" }}
                    },
                    "number_of_remove": {
                        "filter": { "term": { "operation.keyword": "REMOVE" }}
                    }
                }
            }
        }
