class AggregationsMaker:
    def __init__(self):
        self.constant_aggs = {
            "group_by": {
                "aggs": {
                    "number_of_users": {
                        "cardinality": {
                            "field": "user.keyword"
                        }
                    },
                    "number_of_methods": {
                        "cardinality": {
                            "field": "method.keyword"
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
                    },
                    "group_by_first_nested": {
                        "terms": {
                            "field": "user.keyword"
                        },
                        "aggs": {
                            "group_by_second_nested": {
                                "date_histogram": {
                                    "field": "datetime",
                                    "interval": "day"
                                },
                                "aggs": {
                                    "activity_days": {
                                        "cardinality": {
                                            "field": "dataset.keyword"
                                        }
                                    }
                                }
                            },
                            "group_by_first_nested_activitydays": {
                                "sum_bucket": {
                                    "buckets_path": "group_by_second_nested>activity_days.value"
                                }
                            }
                        }
                    },
                    "group_by_activitydays": {
                        "sum_bucket": {
                            "buckets_path": "group_by_first_nested>group_by_first_nested_activitydays"
                        }
                    }
                }
            }
        }

    def get_aggs(self, analysis_method):
        self.generated_aggs = self.constant_aggs
        self._add_group_by(analysis_method)
        self._add_nested_aggs(analysis_method)
        return self.generated_aggs

    def _add_nested_aggs(self, analysis_method):
        # Correctly add sub aggs so analysis_method not in them
        pass

    def _add_group_by(self, analysis_method):
        # Add correct group_by dict dependent on analysis_method (time produces a histogram)
        if analysis_method == "methods":
            self.generated_aggs["group_by"]["terms"] = {}
            self.generated_aggs["group_by"]["terms"]["field"] = "method.keyword"
        if analysis_method == "timeline":
            self.generated_aggs["group_by"]["date_histogram"] = {}
            self.generated_aggs["group_by"]["date_histogram"]["field"] =  "datetime"
            self.generated_aggs["group_by"]["date_histogram"]["interval"] =  "month"
        if analysis_method == "dataset":
            self.generated_aggs["group_by"]["terms"] = {}
            self.generated_aggs["group_by"]["terms"]["field"] = "dataset.keyword"
        if analysis_method == "user":
            self.generated_aggs["group_by"]["terms"] = {}
            self.generated_aggs["group_by"]["terms"]["field"] = "user.keyword"
