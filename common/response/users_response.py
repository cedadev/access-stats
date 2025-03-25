import bitmath

from common.response.file_response import FileResponse


class UsersResponse(FileResponse):
    def get_headings(self):
        return ["User", "Country", "Methods", "Datasets", "Accesses", "Size", "Activity Days"]

    def _write_xlsx(self, json_data, worksheet, date_format):
        worksheet.set_column(0, 0, 27)
        worksheet.set_column(2, 2, 11)
        worksheet.set_column(3, 2, 24)
        worksheet.set_column(7, 8, 11)
        for number, heading in enumerate(self.get_headings()):
            worksheet.write_string(0, number, heading)
        for row, result in enumerate(json_data["results"], start = 1):
            worksheet.write_string(row, 0, result)
            worksheet.write_string(row, 1, json_data["results"][result]["country"])
            worksheet.write_number(row, 4, json_data["results"][result]["methods"])
            worksheet.write_number(row, 5, json_data["results"][result]["datasets"])
            worksheet.write_number(row, 6, json_data["results"][result]["accesses"])
            size = bitmath.parse_string(f'{str(json_data["results"][result]["size"])}B').best_prefix(bitmath.NIST).format("{value:.1f} {unit}")
            worksheet.write_string(row, 7, size)
            worksheet.write_number(row, 8, json_data["results"][result]["activitydays"])
