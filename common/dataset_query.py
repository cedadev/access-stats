from common.query_builder import QueryBuilder

class DatasetQuery(QueryBuilder):
    def __init__(self, filters, analysis_method, after_key):
        self.after_key = after_key
        super().__init__(filters, analysis_method)

    def get_size(self):
        return 0

    def update_aggs(self):
        self.grand_totals()
        self.group_by()

    def group_by_main(self):
        if self.after_key is None:
            self.generated_aggs["group_by"]["terms"] = {}
            self.generated_aggs["group_by"]["terms"]["field"] = "dataset.keyword"
            self.generated_aggs["group_by"]["terms"]["size"] = 500
        else:
            self.generated_aggs["group_by"]["composite"] = {}
            self.generated_aggs["group_by"]["composite"]["size"] = 500
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
