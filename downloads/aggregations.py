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
        if analysis_method != "user":
            self.generated_aggs = self.constant_aggs
        else:
            self.generated_aggs = {}
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

        if analysis_method == "user":
            self.generated_aggs["group_by_field"] = {}
            self.generated_aggs["group_by_field"]["terms"] = {}
            self.generated_aggs["group_by_field"]["terms"]["field"] = "institute.field.keyword"
            self.generated_aggs["group_by_field"]["aggs"] = {}
            self.generated_aggs["group_by_field"]["aggs"]["users"] = {}
            self.generated_aggs["group_by_field"]["aggs"]["users"]["cardinality"] = {}
            self.generated_aggs["group_by_field"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

            self.generated_aggs["group_by_country"] = {}
            self.generated_aggs["group_by_country"]["terms"] = {}
            self.generated_aggs["group_by_country"]["terms"]["field"] = "institute.isocode.keyword"
            self.generated_aggs["group_by_country"]["aggs"] = {}
            self.generated_aggs["group_by_country"]["aggs"]["users"] = {}
            self.generated_aggs["group_by_country"]["aggs"]["users"]["cardinality"] = {}
            self.generated_aggs["group_by_country"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

            self.generated_aggs["group_by_institute_type"] = {}
            self.generated_aggs["group_by_institute_type"]["terms"] = {}
            self.generated_aggs["group_by_institute_type"]["terms"]["field"] = "institute.institute_type.keyword"
            self.generated_aggs["group_by_institute_type"]["aggs"] = {}
            self.generated_aggs["group_by_institute_type"]["aggs"]["users"] = {}
            self.generated_aggs["group_by_institute_type"]["aggs"]["users"]["cardinality"] = {}
            self.generated_aggs["group_by_institute_type"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

            self.generated_aggs["group_by_oda_type"] = {}
            self.generated_aggs["group_by_oda_type"]["terms"] = {}
            self.generated_aggs["group_by_oda_type"]["terms"]["field"] = "country.oda_country.keyword"
            self.generated_aggs["group_by_oda_type"]["aggs"] = {}
            self.generated_aggs["group_by_oda_type"]["aggs"]["users"] = {}
            self.generated_aggs["group_by_oda_type"]["aggs"]["users"]["cardinality"] = {}
            self.generated_aggs["group_by_oda_type"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

            self.generated_aggs["group_by_area"] = {}
            self.generated_aggs["group_by_area"]["terms"] = {}
            self.generated_aggs["group_by_area"]["terms"]["field"] = "country.area.keyword"
            self.generated_aggs["group_by_area"]["aggs"] = {}
            self.generated_aggs["group_by_area"]["aggs"]["users"] = {}
            self.generated_aggs["group_by_area"]["aggs"]["users"]["cardinality"] = {}
            self.generated_aggs["group_by_area"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

        if analysis_method == "users" or analysis_method == "users-limited":
            self.generated_aggs["group_by"]["aggs"]["country"] = {}
            self.generated_aggs["group_by"]["aggs"]["country"]["terms"] = {}
            self.generated_aggs["group_by"]["aggs"]["country"]["terms"]["field"] = "institute.isocode.keyword"
            self.generated_aggs["group_by"]["aggs"]["field"] = {}
            self.generated_aggs["group_by"]["aggs"]["field"]["terms"] = {}
            self.generated_aggs["group_by"]["aggs"]["field"]["terms"]["field"] = "institute.field.keyword"
            self.generated_aggs["group_by"]["aggs"]["institute_type"] = {}
            self.generated_aggs["group_by"]["aggs"]["institute_type"]["terms"] = {}
            self.generated_aggs["group_by"]["aggs"]["institute_type"]["terms"]["field"] = "institute.institute_type.keyword"

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
