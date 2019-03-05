from common.file_response import FileResponse


class DatasetResponse(FileResponse):
    def get_headings(self):
        return ["Dataset", "Users", "Methods", "Accesses", "Size", "Activity Days"]
