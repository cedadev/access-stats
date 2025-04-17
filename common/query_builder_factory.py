from common.es_queries.methods_query import MethodsQuery
from common.es_queries.timeline_query import TimelineQuery
from common.es_queries.dataset_query import DatasetQuery
from common.es_queries.user_query import UserQuery
from common.es_queries.users_query import UsersQuery
from common.es_queries.trace_query import TraceQuery

class QueryBuilderFactory:
    def get(self, filters, analysis_method, after_key):
        if analysis_method == "methods":
            return MethodsQuery(filters, analysis_method)
        if analysis_method == "timeline":
            return TimelineQuery(filters, analysis_method)
        if analysis_method == "dataset":
            return DatasetQuery(filters, analysis_method, after_key)
        if analysis_method == "user":
            return UserQuery(filters, analysis_method, after_key)
        if analysis_method == "users":
            return UsersQuery(filters, analysis_method, after_key)
        if analysis_method == "trace":
            return TraceQuery(filters, analysis_method)
        raise RuntimeError("Invalid analysis method")
