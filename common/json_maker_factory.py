from common.json.methods_json import MethodsJson
from common.json.timeline_json import TimelineJson
from common.json.dataset_json import DatasetJson
from common.json.user_json import UserJson
from common.json.users_json import UsersJson
from common.json.trace_json import TraceJson

class JsonMakerFactory:
    def get(self, filters, analysis_method):
        if analysis_method == "methods":
            return MethodsJson(filters, analysis_method)
        if analysis_method == "timeline":
            return TimelineJson(filters, analysis_method)
        if analysis_method == "dataset":
            return DatasetJson(filters, analysis_method)
        if analysis_method == "user":
            return UserJson(filters, analysis_method)
        if analysis_method == "users":
            return UsersJson(filters, analysis_method)
        if analysis_method == "trace":
            return TraceJson(filters, analysis_method)
        raise RuntimeError("Invalid analysis method")
