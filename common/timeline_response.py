from common.file_response import FileResponse


class TimelineResponse(FileResponse):
    def get_headings(self):
        return ["Timeline", "Users", "Methods", "Dataset", "Accesses", "Size", "Activity Days"]
