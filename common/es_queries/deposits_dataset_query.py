from common.es_queries.deposits_query_builder import DepositsQueryBuilder
from common.es_queries.dataset_query import DatasetQuery

class DepositsDatasetQuery(DepositsQueryBuilder, DatasetQuery):
    def update_aggs(self):
        self.grand_totals()
        self.group_by()

    def group_by_main(self):
        self.generated_aggs["group_by"]["composite"] = {}
        self.generated_aggs["group_by"]["composite"]["size"] = 10000
        if self.after_key:
            self.generated_aggs["group_by"]["composite"]["after"] = self.after_key
        self.generated_aggs["group_by"]["composite"]["sources"] = []
        self.generated_aggs["group_by"]["composite"]["sources"].append({
            "dataset": {
                "terms": {
                    "field": "dataset.keyword.terms.value"
                }
            }
        })
    