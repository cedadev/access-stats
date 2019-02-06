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
                        "aggs": {
                            "group_by_second_nested": {
                                "aggs": {
                                    "activity_days": {
                                        "cardinality": {}
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


    def get_aggs(self, analysis_method, after_key=None):
        self.generated_aggs = self.constant_aggs
        self._add_group_by(analysis_method, after_key)
        self._add_nested_aggs(analysis_method)
        return self.generated_aggs

    def _add_nested_aggs(self, analysis_method):
        # Correctly add sub aggs so analysis_method not in them
        if analysis_method == "methods":
            self._add_nested_aggs_methods()
        if analysis_method == "timeline":
            self._add_nested_aggs_timeline()
        if analysis_method == "dataset" or analysis_method == "dataset-limited":
            self._add_nested_aggs_dataset()
        if analysis_method == "users" or analysis_method == "users-limited":
            self._add_nested_aggs_users()

    def _add_nested_aggs_methods(self):
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"]["field"] = "user.keyword"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["field"]  = "datetime"
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["interval"]  = "day"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["aggs"]["activity_days"]["cardinality"]["field"] = "dataset.keyword"

    def _add_nested_aggs_timeline(self):
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"]["field"] = "user.keyword"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["terms"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["terms"]["field"] = "method.keyword"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["aggs"]["activity_days"]["cardinality"]["field"] = "dataset.keyword"
    
    def _add_nested_aggs_dataset(self):
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"]["field"] = "user.keyword"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["field"]  = "datetime"
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["interval"]  = "day"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["aggs"]["activity_days"]["cardinality"]["field"] = "method.keyword"

    def _add_nested_aggs_users(self):
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"]["field"] = "method.keyword"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["field"]  = "datetime"
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["interval"]  = "day"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["aggs"]["activity_days"]["cardinality"]["field"] = "dataset.keyword"

    def _add_group_by(self, analysis_method, after_key=None):
        # Add correct group_by dict dependent on analysis_method (time produces a histogram)
        if analysis_method == "methods":
            self.generated_aggs["group_by"]["terms"] = {}
            self.generated_aggs["group_by"]["terms"]["field"] = "method.keyword"
            self.generated_aggs["group_by"]["terms"]["size"] = 30
        if analysis_method == "timeline":
            self.generated_aggs["group_by"]["date_histogram"] = {}
            self.generated_aggs["group_by"]["date_histogram"]["field"] =  "datetime"
            self.generated_aggs["group_by"]["date_histogram"]["interval"] =  "month"
        if analysis_method == "dataset":
            self.generated_aggs["group_by"]["composite"] = {}
            self.generated_aggs["group_by"]["composite"]["size"] = 1000
            if after_key:
                self.generated_aggs["group_by"]["composite"]["after"] = after_key
            self.generated_aggs["group_by"]["composite"]["sources"] = []
            self.generated_aggs["group_by"]["composite"]["sources"].append({
                "dataset": {
                    "terms": {
                        "field": "dataset.keyword"
                    }
                }
            })
        if analysis_method == "dataset-limited":
            self.generated_aggs["group_by"]["terms"] = {}
            self.generated_aggs["group_by"]["terms"]["field"] = "dataset.keyword"
            self.generated_aggs["group_by"]["terms"]["size"] = 500
        if analysis_method == "users":
            self.generated_aggs["group_by"]["composite"] = {}
            self.generated_aggs["group_by"]["composite"]["size"] = 1000
            if after_key:
                self.generated_aggs["group_by"]["composite"]["after"] = after_key
            self.generated_aggs["group_by"]["composite"]["sources"] = []
            self.generated_aggs["group_by"]["composite"]["sources"].append({
                "user": {
                    "terms": {
                        "field": "user.keyword"
                    }
                }
            })
        if analysis_method == "users-limited":
            self.generated_aggs["group_by"]["terms"] = {}
            self.generated_aggs["group_by"]["terms"]["field"] = "user.keyword"
            self.generated_aggs["group_by"]["terms"]["size"] = 500
