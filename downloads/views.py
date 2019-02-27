import csv, io, bitmath
import dateutil.parser

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView

from xlsxwriter.workbook import Workbook

from downloads.forms import FilterForm
from downloads.json import QueryElasticSearch

valid_analysis_methods = ["methods","timeline","dataset","dataset-limited","user","users","users-limited","trace"]

default_404_response = HttpResponseNotFound('<h1>404 - Not found</h1>')

class IndexView(TemplateView):
    template_name = "downloads/index.html"
    
    def get(self, request):
        if request.GET:
            form = FilterForm(request.GET)
        else:
            form = FilterForm()
        
        return render(request, self.template_name, {'form': form})

class JsonView(TemplateView):
    def get_data_from_es(self, filters, analysis_method):
        return QueryElasticSearch().get_data(filters, analysis_method)

    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method not in valid_analysis_methods or not form.is_valid():
            return default_404_response
        return JsonResponse(self.get_data_from_es(form.cleaned_data, analysis_method), json_dumps_params={'indent': 2})

class TxtView(TemplateView):
    def generate_text_file(self, filters, analysis_method):
        json_data = QueryElasticSearch().get_data(filters, analysis_method)
        logs = ""
        for log in json_data["logs"]:
            logs += f"{log}\n"
        return logs

    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if analysis_method != "trace" or not form.is_valid():
            return default_404_response
        return HttpResponse(self.generate_text_file(form.cleaned_data, analysis_method), content_type="text/plain")

class FileMaker(TemplateView):
    methods_headings = ["Method", "Users", "Dataset", "Accesses", "Size", "Activity Days"]
    timeline_headings = ["Timeline", "Users", "Methods", "Dataset", "Accesses", "Size", "Activity Days"]
    dataset_headings = ["Dataset", "Users", "Methods", "Accesses", "Size", "Activity Days"]
    users_headings = ["User", "Country", "Institute type", "Field", "Methods", "Datasets", "Accesses", "Size", "Activity Days"]

    def make_filename(self, request, analysis_method, file_ending):
        filename = f'{analysis_method}-'
        if request.GET["start"]:
            filename += f'{request.GET["start"]}-'
        if request.GET["end"]:
            filename += f'{request.GET["end"]}-'
        if request.GET["user"]:
            filename += f'{request.GET["user"]}-'
        if request.GET["dataset"]:
            filename += f'{request.GET["dataset"]}-'
        if request.GET["method"]:
            filename += f'{request.GET["method"]}-'
        filename += f'{request.GET["anon"]}.{file_ending}'
        return filename
    
class CsvView(FileMaker):
    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if (analysis_method != "methods" and analysis_method != "timeline" and analysis_method != "dataset" and analysis_method != "users") or not form.is_valid():
            return default_404_response
        response = HttpResponse(content_type="text/csv")
        
        response['Content-Disposition'] = f'attachment; filename={self.make_filename(request, analysis_method, file_ending="csv")}'
        writer = csv.writer(response)
        self.write_csv_file(form.cleaned_data, analysis_method, writer)

        return response

    def write_csv_file(self, filters, analysis_method, writer):
        json_data = QueryElasticSearch().get_data(filters, analysis_method)
        if analysis_method == "methods":
            writer.writerow(self.methods_headings)
        if analysis_method == "timeline":
            writer.writerow(self.timeline_headings)
        if analysis_method == "dataset":
            writer.writerow(self.dataset_headings)
        if analysis_method == "users":
            writer.writerow(self.users_headings)

        for result in json_data["results"]:
            line = [result]
            for value in json_data["results"][result].values():
                line.append(value)
            writer.writerow(line)
        return

class XlsxView(FileMaker):
    def get(self, request, analysis_method):
        form = FilterForm(request.GET)
        if (analysis_method != "dataset" and analysis_method != "timeline" and analysis_method != "methods" and analysis_method != "users") or not form.is_valid():
            return default_404_response
        
        output = io.BytesIO()
        workbook = Workbook(output, {"in_memory": True, 'remove_timezone': True})
        worksheet = workbook.add_worksheet()
        date_format = workbook.add_format({'num_format': 'yyyymm'})
        self.write_xlsx_file(form.cleaned_data, analysis_method, worksheet, date_format)
        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f'attachment; filename={self.make_filename(request, analysis_method, file_ending="xlsx")}'

        return response

    def write_xlsx_file(self, filters, analysis_method, writer, date_format):
        json_data = QueryElasticSearch().get_data(filters, analysis_method)
        if analysis_method == "methods":
            writer.set_column(0, 0, 22)
            writer.set_column(1, 5, 11)
            writer.set_column(3, 4, 17)
            for number, heading in enumerate(self.methods_headings):
                writer.write_string(0, number, heading)
            for row, result in enumerate(json_data["results"], start = 1):
                writer.write_string(row, 0, result)
                writer.write_number(row, 1, json_data["results"][result]["users"])
                writer.write_number(row, 2, json_data["results"][result]["datasets"])
                writer.write_number(row, 3, json_data["results"][result]["accesses"])
                size = bitmath.parse_string(f'{str(json_data["results"][result]["size"])}B').best_prefix(bitmath.NIST).format("{value:.1f} {unit}")
                writer.write_string(row, 4, size)
                writer.write_number(row, 5, json_data["results"][result]["activitydays"])

        if analysis_method == "timeline":
            writer.set_column(0, 6, 11)
            writer.set_column(5, 5, 17)
            for number, heading in enumerate(self.timeline_headings):
                writer.write_string(0, number, heading)
            for row, result in enumerate(json_data["results"], start = 1):
                month = dateutil.parser.parse(result)
                writer.write_datetime(row, 0, month, date_format)
                writer.write_number(row, 1, json_data["results"][result]["users"])
                writer.write_number(row, 2, json_data["results"][result]["methods"])
                writer.write_number(row, 3, json_data["results"][result]["datasets"])
                writer.write_number(row, 4, json_data["results"][result]["accesses"])
                size = bitmath.parse_string(f'{str(json_data["results"][result]["size"])}B').best_prefix(bitmath.NIST).format("{value:.1f} {unit}")
                writer.write_string(row, 5, size)
                writer.write_number(row, 6, json_data["results"][result]["activitydays"])

        if analysis_method == "dataset":
            writer.set_column(0, 0, 74)
            writer.set_column(1, 5, 11)
            for number, heading in enumerate(self.dataset_headings):
                writer.write_string(0, number, heading)
            for row, result in enumerate(json_data["results"], start = 1):
                writer.write_string(row, 0, result)
                writer.write_number(row, 1, json_data["results"][result]["users"])
                writer.write_number(row, 2, json_data["results"][result]["methods"])
                writer.write_number(row, 3, json_data["results"][result]["accesses"])
                size = bitmath.parse_string(f'{str(json_data["results"][result]["size"])}B').best_prefix(bitmath.NIST).format("{value:.1f} {unit}")
                writer.write_string(row, 4, size)
                writer.write_number(row, 5, json_data["results"][result]["activitydays"])

        if analysis_method == "users":
            writer.set_column(0, 0, 27)
            writer.set_column(2, 2, 11)
            writer.set_column(3, 2, 24)
            writer.set_column(7, 8, 11)
            for number, heading in enumerate(self.users_headings):
                writer.write_string(0, number, heading)
            for row, result in enumerate(json_data["results"], start = 1):
                writer.write_string(row, 0, result)
                writer.write_string(row, 1, json_data["results"][result]["country"])
                writer.write_string(row, 2, json_data["results"][result]["institute_type"])
                writer.write_string(row, 3, json_data["results"][result]["field"])
                writer.write_number(row, 4, json_data["results"][result]["methods"])
                writer.write_number(row, 5, json_data["results"][result]["datasets"])
                writer.write_number(row, 6, json_data["results"][result]["accesses"])
                size = bitmath.parse_string(f'{str(json_data["results"][result]["size"])}B').best_prefix(bitmath.NIST).format("{value:.1f} {unit}")
                writer.write_string(row, 7, size)
                writer.write_number(row, 8, json_data["results"][result]["activitydays"])

        return
    