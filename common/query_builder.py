class QueryBuilder:
    def __init__(self, filters, analysis_method):
        self.filters = filters
        self.analysis_method = analysis_method
        
    def query(self):
        self.generate_query()
        return self.generated_query

    def generate_query(self):
        self.generated_query = self.base_query()
        self.update_filters()
        self.update_aggs()

    def get_size(self):
        return NotImplementedError

    def update_aggs(self):
        return NotImplementedError
    
    def base_query(self):
        return {
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [
                        {
                            "match": {
                                "method.keyword.terms.value": "deposits"
                            }
                        }
                    ],
                    "should": [],
                    "filter": {
                        "range": {
                            "datetime.date_histogram.timestamp": {
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
            self.generated_query["query"]["bool"]["filter"]["range"]["datetime.date_histogram.timestamp"]["gte"] = self.filters["start"]
        if self.filters["end"]:
            self.generated_query["query"]["bool"]["filter"]["range"]["datetime.date_histogram.timestamp"]["lte"] = self.filters["end"]
        if self.filters["user"]:
            self.generated_query["query"]["bool"]["must"].append({
                        "match_phrase": {
                            "user.keyword.terms.value": self.filters["user"]
                        }
                    })
        if self.filters["dataset"]:
            self.generated_query["query"]["bool"]["must"].append({
                        "match_phrase_prefix": {
                            "dataset.keyword.terms.value": self.filters["dataset"]
                        }
                    })
        if self.filters["method"]:
            self.generated_query["query"]["bool"]["must"].append({
                        "match_phrase": {
                            "method.keyword.terms.value": self.filters["method"]
                        }
                    })
        if self.filters["anon"]:
            if self.filters["anon"] == "anon":
                self.generated_query["query"]["bool"]["must"].append({
                            "match_phrase_prefix": {
                                "user.keyword.terms.value": "anonymous@"
                            }
                        })
            if self.filters["anon"] == "non-anon":
                self.generated_query["query"]["bool"]["must_not"].append({
                            "match_phrase_prefix": {
                                "user.keyword.terms.value": "anonymous@"
                            }
                        })

    # Functions that add aggregations to the generated query:
    # To be called per subclass in update_aggs()
    def grand_totals(self):
        self.generated_query["aggs"].update({
            "grand_total_users": {
                "cardinality": {
                    "field": "user.keyword.terms.value"
                }
            },
            "grand_total_methods": {
                "cardinality": {
                    "field": "method.keyword.terms.value"
                }
            },
            "grand_total_datasets": {
                "cardinality": {
                    "field": "dataset.keyword.terms.value"
                }
            },
            "grand_total_size": {
                "sum": {
                    "field": "size.sum.value"
                }
            }
        })
    
    def group_by(self):
        self.generated_aggs = self.base_aggs()
        self.group_by_main()
        self.generated_query["aggs"].update(self.generated_aggs)

    def group_by_main(self):
        return NotImplementedError

    def base_aggs(self):
        return {
            "group_by": {
                "aggs": {
                    "number_of_users": {
                        "cardinality": {
                            "field": "user.keyword.terms.value"
                        }
                    },
                    "number_of_methods": {
                        "cardinality": {
                            "field": "method.keyword.terms.value"
                        }
                    },
                    "number_of_datasets": {
                        "cardinality": {
                            "field": "dataset.keyword.terms.value"
                        }
                    },
                    "number_of_accesses": {
                        "sum": {
                            "field": "method.keyword.terms._count"
                        }
                    },
                    "total_size": {
                        "sum": {
                            "field": "size.sum.value"
                        }
                    }
                }
            }
        }
