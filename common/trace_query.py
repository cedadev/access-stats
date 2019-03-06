from common.query_builder import QueryBuilder

class TraceQuery(QueryBuilder):
    def get_size(self):
        return 1000

    def update_aggs(self):
        return