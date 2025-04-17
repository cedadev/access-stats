import bitmath, dateutil.parser

from common.response.file_response import FileResponse


class TimelineResponse(FileResponse):
    def get_headings(self):
        return ["Timeline", "Users", "Methods", "Dataset", "Accesses", "Size", "Countries", "Activity Days"]

    def _write_xlsx(self, json_data, worksheet, date_format):
        worksheet.set_column(0, 6, 11)
        worksheet.set_column(5, 5, 17)
        for number, heading in enumerate(self.get_headings()):
            worksheet.write_string(0, number, heading)
        for row, result in enumerate(json_data["results"], start = 1):
            month = dateutil.parser.parse(result)
            worksheet.write_datetime(row, 0, month, date_format)
            worksheet.write_number(row, 1, json_data["results"][result]["users"])
            worksheet.write_number(row, 2, json_data["results"][result]["methods"])
            worksheet.write_number(row, 3, json_data["results"][result]["datasets"])
            worksheet.write_number(row, 4, json_data["results"][result]["accesses"])
            size = bitmath.parse_string(f'{str(json_data["results"][result]["size"])}B').best_prefix(bitmath.NIST).format("{value:.1f} {unit}")
            worksheet.write_string(row, 5, size)
            worksheet.write_number(row, 6, json_data["results"][result]["countries"])
            worksheet.write_number(row, 7, json_data["results"][result]["activitydays"])
