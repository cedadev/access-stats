from common.deposits_query_builder import DepositsQueryBuilder
from common.timeline_query import TimelineQuery

class DepositsTimelineQuery(DepositsQueryBuilder, TimelineQuery):
    def update_aggs(self):
        self.grand_totals()
        self.group_by()

    def group_by_main(self):
            self.generated_aggs["group_by"]["date_histogram"] = {}
            self.generated_aggs["group_by"]["date_histogram"]["field"] =  "datetime.date_histogram.timestamp"
            self.generated_aggs["group_by"]["date_histogram"]["interval"] =  "day"

    