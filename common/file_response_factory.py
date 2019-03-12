from common.methods_response import MethodsResponse
from common.timeline_response import TimelineResponse
from common.deposits_timeline_response import DepositsTimelineResponse
from common.dataset_response import DatasetResponse
from common.deposits_dataset_response import DepositsDatasetResponse
from common.users_response import UsersResponse


class FileResponseFactory:
    def __init__(self, deposits=False):
        self.deposits = deposits

    def get(self, filters, analysis_method):
        if analysis_method == "methods":
            return MethodsResponse(filters, analysis_method)
        if analysis_method == "timeline" and not self.deposits:
            return TimelineResponse(filters, analysis_method)
        if analysis_method == "timeline" and self.deposits:
            return DepositsTimelineResponse(filters, analysis_method)
        if analysis_method == "dataset" and not self.deposits:
            return DatasetResponse(filters, analysis_method)
        if analysis_method == "dataset" and self.deposits:
            return DepositsDatasetResponse(filters, analysis_method)
        if analysis_method == "users":
            return UsersResponse(filters, analysis_method)
        raise RuntimeError("Invalid analysis method for creating a file")
