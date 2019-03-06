import csv, io

from xlsxwriter.workbook import Workbook

from django.http import HttpResponse

#TODO: Rewrite
from downloads.json import QueryElasticSearch


class FileResponse:
    def __init__(self, filters, analysis_method):
        self.filters = filters
        self.analysis_method = analysis_method

    def get_headings(self):
        raise NotImplementedError

    def get_filename(self, file_ending):
        filename = f'{self.analysis_method}'
        for value in self.filters.values():
            if value:
                filename += f'-{value}'
        filename += f'.{file_ending}'
        return filename

    def make_csv(self):
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename={self.get_filename("csv")}'
        writer = csv.writer(response)

        ##TODO: Rewrite
        json_data = QueryElasticSearch().get_data(self.filters, self.analysis_method)

        writer.writerow(self.get_headings())
        for result in json_data["results"]:
            line = [result]
            for value in json_data["results"][result].values():
                line.append(value)
            writer.writerow(line)

        return response

    def make_xlsx(self):
        ##TODO: Rewrite
        json_data = QueryElasticSearch().get_data(self.filters, self.analysis_method)

        output = io.BytesIO()
        workbook = Workbook(output, {"in_memory": True, 'remove_timezone': True})
        worksheet = workbook.add_worksheet()
        date_format = workbook.add_format({'num_format': 'yyyymm'})
        
        self._write_xlsx(json_data, worksheet, date_format)

        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f'attachment; filename={self.get_filename("xlsx")}'

        return response


    def _write_xlsx(self, json_data, worksheet, date_format):
        raise NotImplementedError
