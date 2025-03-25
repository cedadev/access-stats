from common.es_queries.methods_query import MethodsQuery
from common.es_queries.timeline_query import TimelineQuery
from common.es_queries.dataset_query import DatasetQuery
from common.es_queries.user_query import UserQuery
from common.es_queries.users_query import UsersQuery
from common.es_queries.trace_query import TraceQuery
from common.obsolete_deposits.deposits_trace_query import DepositsTraceQuery

class QueryBuilderFactory:
    def __init__(self, deposits = False):
            self.deposits = deposits

    def get(self, filters, analysis_method, after_key):
        if analysis_method == "methods":
            return MethodsQuery(filters, analysis_method)
        if analysis_method == "timeline" and not self.deposits:
            return TimelineQuery(filters, analysis_method)
        if analysis_method == "dataset" and not self.deposits:
            return DatasetQuery(filters, analysis_method, after_key)
        if analysis_method == "user":
            return UserQuery(filters, analysis_method)
        if analysis_method == "users":
            return UsersQuery(filters, analysis_method, after_key)
        if analysis_method == "trace" and not self.deposits:
            return TraceQuery(filters, analysis_method)
        if analysis_method == "trace" and self.deposits:
            return DepositsTraceQuery(filters, analysis_method)
        raise RuntimeError("Invalid analysis method")
