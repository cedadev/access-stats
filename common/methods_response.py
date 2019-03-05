from common.file_response import FileResponse


class MethodsResponse(FileResponse):
    def get_headings(self):
        return ["Method", "Users", "Dataset", "Accesses", "Size", "Activity Days"]
