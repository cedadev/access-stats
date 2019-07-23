from common.query_builder import QueryBuilder

class TimelineQuery(QueryBuilder):
    def get_size(self):
        return 0

    def update_aggs(self):
        self.grand_totals()
        self.group_by()

    def group_by_main(self):
        self.generated_aggs["group_by"]["date_histogram"] = {}
        self.generated_aggs["group_by"]["date_histogram"]["field"] =  "datetime.date_histogram.timestamp"
        self.generated_aggs["group_by"]["date_histogram"]["interval"] =  "month"
