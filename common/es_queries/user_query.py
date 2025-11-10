from common.query_builder import QueryBuilder

class UserQuery(QueryBuilder):
    def __init__(self, filters, analysis_method, after_key):
        self.after_key = after_key
        super().__init__(filters, analysis_method)

    def get_size(self):
        return 0

    def update_aggs(self):
        self.group_by()

    def group_by_main(self):
        self.generated_aggs["group_by_country"] = {}

        self.generated_aggs["group_by_country"]["terms"] = {}
        self.generated_aggs["group_by_country"]["terms"]["size"] = 1000
        self.generated_aggs["group_by_country"]["terms"]["field"] = "country.keyword.terms.value"
        self.generated_aggs["group_by_country"]["aggs"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"]["cardinality"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword.terms.value"

    def base_aggs(self):
        return {}
