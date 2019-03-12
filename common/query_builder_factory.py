from common.methods_query import MethodsQuery
from common.timeline_query import TimelineQuery
from common.deposits_timeline_query import DepositsTimelineQuery
from common.dataset_query import DatasetQuery
from common.deposits_dataset_query import DepositsDatasetQuery
from common.user_query import UserQuery
from common.users_query import UsersQuery
from common.trace_query import TraceQuery
from common.deposits_trace_query import DepositsTraceQuery

class QueryBuilderFactory:
    def __init__(self, deposits = False):
            self.deposits = deposits

    def get(self, filters, analysis_method, after_key):
        if analysis_method == "methods":
            return MethodsQuery(filters, analysis_method)
        if analysis_method == "timeline" and not self.deposits:
            return TimelineQuery(filters, analysis_method)
        if analysis_method == "timeline" and self.deposits:
            return DepositsTimelineQuery(filters, analysis_method)
        if analysis_method in ["dataset", "dataset-limited"] and not self.deposits:
            return DatasetQuery(filters, analysis_method, after_key)
        if analysis_method in ["dataset", "dataset-limited"] and self.deposits:
            return DepositsDatasetQuery(filters, analysis_method, after_key)
        if analysis_method == "user":
            return UserQuery(filters, analysis_method)
        if analysis_method in ["users", "users-limited"]:
            return UsersQuery(filters, analysis_method, after_key)
        if analysis_method == "trace" and not self.deposits:
            return TraceQuery(filters, analysis_method)
        if analysis_method == "trace" and self.deposits:
            return DepositsTraceQuery(filters, analysis_method)
        raise RuntimeError("Invalid analysis method")
