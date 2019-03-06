from common.query_builder import QueryBuilder

class MethodsQuery(QueryBuilder):
    def get_size(self):
        return 0

    def update_aggs(self):
        self.grand_totals()
        self.grand_total_activity_days()
        self.group_by()

    def group_by_main(self):
        self.generated_aggs["group_by"]["terms"] = {}
        self.generated_aggs["group_by"]["terms"]["field"] = "method.keyword"
        self.generated_aggs["group_by"]["terms"]["size"] = 30

    def group_by_nested(self):
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["terms"]["field"] = "user.keyword"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"] = {}
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["field"]  = "datetime"
        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["date_histogram"]["interval"]  = "day"

        self.generated_aggs["group_by"]["aggs"]["group_by_first_nested"]["aggs"]["group_by_second_nested"]["aggs"]["activity_days"]["cardinality"]["field"] = "dataset.keyword"
