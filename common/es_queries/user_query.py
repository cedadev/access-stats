from common.query_builder import QueryBuilder

class UserQuery(QueryBuilder):
    def get_size(self):
        return 0

    def update_aggs(self):
        self.group_by()

    def group_by_main(self):
        self.generated_aggs["group_by_country"] = {}
        self.generated_aggs["group_by_country"]["terms"] = {}
        self.generated_aggs["group_by_country"]["terms"]["field"] = "country.terms.value"
        self.generated_aggs["group_by_country"]["aggs"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"]["cardinality"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"]["cardinality"]["field"] = "user.terms.value"

    def base_aggs(self):
        return {}
