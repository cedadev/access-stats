from common.methods_json import MethodsJson
from common.timeline_json import TimelineJson
from common.deposits_timeline_json import DepositsTimelineJson
from common.dataset_json import DatasetJson
from common.deposits_dataset_json import DepositsDatasetJson
from common.user_json import UserJson
from common.users_json import UsersJson
from common.trace_json import TraceJson
from common.deposits_trace_json import DepositsTraceJson

class JsonMakerFactory:
    def __init__(self, deposits = False):
        self.deposits = deposits

    def get(self, filters, analysis_method):
        if analysis_method == "methods":
            return MethodsJson(filters, analysis_method)
        if analysis_method == "timeline" and not self.deposits:
            return TimelineJson(filters, analysis_method)
        if analysis_method == "timeline" and self.deposits:
            return DepositsTimelineJson(filters, analysis_method)
        if analysis_method in ["dataset", "dataset-limited"] and not self.deposits:
            return DatasetJson(filters, analysis_method)
        if analysis_method in ["dataset", "dataset-limited"] and self.deposits:
            return DepositsDatasetJson(filters, analysis_method)
        if analysis_method == "user":
            return UserJson(filters, analysis_method)
        if analysis_method == "users" or analysis_method == "users-limited":
            return UsersJson(filters, analysis_method)
        if analysis_method == "trace" and not self.deposits:
            return TraceJson(filters, analysis_method)
        if analysis_method == "trace" and self.deposits:
            return DepositsTraceJson(filters, analysis_method)
        raise RuntimeError("Invalid analysis method")
