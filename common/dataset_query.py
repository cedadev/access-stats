from common.query_builder import QueryBuilder

class DatasetQuery(QueryBuilder):
    def __init__(self, filters, analysis_method, after_key):
        self.after_key = after_key
        super().__init__(filters, analysis_method)

    def get_size(self):
        return 0

    def update_aggs(self):
        self.grand_totals()
        if "limited" in self.analysis_method:
            self.grand_total_activity_days()
        self.group_by()

    def group_by_main(self):
        if self.after_key is None:
            self.generated_aggs["group_by"]["terms"] = {}
            self.generated_aggs["group_by"]["terms"]["field"] = "dataset.keyword"
            self.generated_aggs["group_by"]["terms"]["size"] = 500
        else:
            self.generated_aggs["group_by"]["composite"] = {}
            self.generated_aggs["group_by"]["composite"]["size"] = 1000
            if self.after_key:
                self.generated_aggs["group_by"]["composite"]["after"] = self.after_key
            self.generated_aggs["group_by"]["composite"]["sources"] = []
            self.generated_aggs["group_by"]["composite"]["sources"].append({
                "dataset": {
                    "terms": {
                        "field": "dataset.keyword"
                    }
                }
            })

    def group_by_nested(self):
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"]["field"] = "user.keyword"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["field"]  = "datetime"
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["interval"]  = "day"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["aggs"]["activity_days"]["cardinality"]["field"] = "method.keyword"
