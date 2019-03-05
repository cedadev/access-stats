from common.file_response import FileResponse


class UsersResponse(FileResponse):
    def get_headings(self):
        return ["User", "Country", "Institute type", "Field", "Methods", "Datasets", "Accesses", "Size", "Activity Days"]
