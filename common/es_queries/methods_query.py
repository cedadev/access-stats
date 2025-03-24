from common.query_builder import QueryBuilder

class MethodsQuery(QueryBuilder):
    def get_size(self):
        return 0

    def update_aggs(self):
        self.grand_totals()
        self.group_by()

    def group_by_main(self):
        self.generated_aggs["group_by"]["terms"] = {}
        self.generated_aggs["group_by"]["terms"]["field"] = "method.keyword.terms.value"
        self.generated_aggs["group_by"]["terms"]["size"] = 10000
