import csv
from django.http import HttpResponse

#TODO: Rewrite
from downloads.json import QueryElasticSearch


class FileResponse():
    def __init__(self, filters, analysis_method):
        self.filters = filters
        self.analysis_method = analysis_method

    def get_headings(self):
        raise NotImplementedError()

    def get_filename(self, file_ending):
        print(self.filters)  # loop through?
        filename = f'{self.analysis_method}-'
        if self.filters["start"]:
            filename += f'{self.filters["start"]}-'
        if self.filters["end"]:
            filename += f'{self.filters["end"]}-'
        if self.filters["user"]:
            filename += f'{self.filters["user"]}-'
        if self.filters["dataset"]:
            filename += f'{self.filters["dataset"]}-'
        if self.filters["method"]:
            filename += f'{self.filters["method"]}-'
        filename += f'{self.filters["anon"]}.{file_ending}'
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
        raise NotImplementedError()
