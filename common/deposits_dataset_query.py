from common.deposits_query_builder import DepositsQueryBuilder
from common.dataset_query import DatasetQuery

class DepositsDatasetQuery(DepositsQueryBuilder, DatasetQuery):
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
        pass
    