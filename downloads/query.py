from downloads.aggregations import AggregationsMaker

class QueryMaker():
    def generate_query(self, filters, analysis_method, after_key=None):
        if analysis_method == "trace":
            self.generated_query = self._base_small_query()
        elif analysis_method == "user":
            self.generated_query = self._base_medium_query()
        else:
            self.generated_query = self._base_big_query()
        self._update_filters(filters)
        if analysis_method != "trace":
            self._update_aggs(analysis_method, after_key)
        return self.generated_query

    def _update_aggs(self, analysis_method, after_key):
        if analysis_method != "users" and analysis_method != "dataset" and analysis_method != "user":
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

    def _base_medium_query(self):
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
            "aggs": {}
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
