from common.methods_json import MethodsJson
from common.timeline_json import TimelineJson
from common.dataset_json import DatasetJson
from common.user_json import UserJson
from common.users_json import UsersJson
from common.trace_json import TraceJson

class JsonMakerFactory:
    def get(self, filters, analysis_method):
        if analysis_method == "methods":
            return MethodsJson(filters, analysis_method)
        if analysis_method == "timeline":
            return TimelineJson(filters, analysis_method)
        if analysis_method == "dataset" or analysis_method == "dataset-limited":
            return DatasetJson(filters, analysis_method)
        if analysis_method == "user":
            return UserJson(filters, analysis_method)
        if analysis_method == "users" or analysis_method == "users-limited":
            return UsersJson(filters, analysis_method)
        if analysis_method == "trace":
            return TraceJson(filters, analysis_method)
        raise RuntimeError("Invalid analysis method")
