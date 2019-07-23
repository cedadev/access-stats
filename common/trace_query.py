from common.query_builder import QueryBuilder

class TraceQuery(QueryBuilder):
    def get_size(self):
        return 1000

    def update_aggs(self):
        return

    def method(self):
        return "method.keyword"

    def datetime(self):
        return "datetime"

    def user(self):
        return "user.keyword"
    
    def dataset(self):
        return "dataset.keyword"
    
    def size(self):
        return "size"

    def base_aggs(self):
        return
