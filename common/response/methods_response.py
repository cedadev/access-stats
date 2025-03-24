import bitmath

from common.response.file_response import FileResponse


class MethodsResponse(FileResponse):
    def get_headings(self):
        return ["Method", "Users", "Dataset", "Accesses", "Size", "Activity Days"]
    
    def _write_xlsx(self, json_data, worksheet, date_format):
        worksheet.set_column(0, 0, 22)
        worksheet.set_column(1, 5, 11)
        worksheet.set_column(3, 4, 17)
        for number, heading in enumerate(self.get_headings()):
            worksheet.write_string(0, number, heading)
        for row, result in enumerate(json_data["results"], start = 1):
            worksheet.write_string(row, 0, result)
            worksheet.write_number(row, 1, json_data["results"][result]["users"])
            worksheet.write_number(row, 2, json_data["results"][result]["datasets"])
            worksheet.write_number(row, 3, json_data["results"][result]["accesses"])
            size = bitmath.parse_string(f'{str(json_data["results"][result]["size"])}B').best_prefix(bitmath.NIST).format("{value:.1f} {unit}")
            worksheet.write_string(row, 4, size)
            worksheet.write_number(row, 5, json_data["results"][result]["activitydays"])
