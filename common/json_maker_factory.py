from common.json.methods_json import MethodsJson
from common.json.timeline_json import TimelineJson
from common.json.deposits_timeline_json import DepositsTimelineJson
from common.json.dataset_json import DatasetJson
from common.json.deposits_dataset_json import DepositsDatasetJson
from common.json.user_json import UserJson
from common.json.users_json import UsersJson
from common.json.trace_json import TraceJson
from common.json.deposits_trace_json import DepositsTraceJson

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
        if analysis_method == "dataset" and not self.deposits:
            return DatasetJson(filters, analysis_method)
        if analysis_method == "dataset" and self.deposits:
            return DepositsDatasetJson(filters, analysis_method)
        if analysis_method == "user":
            return UserJson(filters, analysis_method)
        if analysis_method == "users":
            return UsersJson(filters, analysis_method)
        if analysis_method == "trace" and not self.deposits:
            return TraceJson(filters, analysis_method)
        if analysis_method == "trace" and self.deposits:
            return DepositsTraceJson(filters, analysis_method)
        raise RuntimeError("Invalid analysis method")
