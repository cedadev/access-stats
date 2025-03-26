from common.response.methods_response import MethodsResponse
from common.response.timeline_response import TimelineResponse
from common.response.dataset_response import DatasetResponse
from common.response.users_response import UsersResponse


class FileResponseFactory:
    def get(self, filters, analysis_method):
        if analysis_method == "methods":
            return MethodsResponse(filters, analysis_method)
        if analysis_method == "timeline":
            return TimelineResponse(filters, analysis_method)
        if analysis_method == "dataset":
            return DatasetResponse(filters, analysis_method)
        if analysis_method == "users":
            return UsersResponse(filters, analysis_method)
        raise RuntimeError("Invalid analysis method for creating a file")
