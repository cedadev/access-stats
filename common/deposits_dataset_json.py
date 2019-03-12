from common.json_maker import JsonMaker

class DepositsDatasetJson(JsonMaker):
    def get_title(self):
        return "Summary of deposits to CEDA archive by dataset"

    def _populate_json(self):
        if self.analysis_method == "dataset":
            response = self.get_elasticsearch_response(after_key = 0, deposits=True)
            self.generated_json["totals"] = {}
            self.generated_json["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
            self.generated_json["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
            self.generated_json["totals"]["deposits"] = response["aggregations"]["grand_total_deposits"]["doc_count"]
            self.generated_json["totals"]["mkdir"] = response["aggregations"]["grand_total_mkdir"]["doc_count"]
            self.generated_json["totals"]["symlink"] = response["aggregations"]["grand_total_symlink"]["doc_count"]
            self.generated_json["totals"]["rmdir"] = response["aggregations"]["grand_total_rmdir"]["doc_count"]
            self.generated_json["totals"]["remove"] = response["aggregations"]["grand_total_remove"]["doc_count"]

            self.generated_json["results"] = {}
            while response["aggregations"]["group_by"]["buckets"] != []:
                for result in response["aggregations"]["group_by"]["buckets"]:
                    self.generated_json["results"][result["key"]["dataset"]] = {}
                    self.generated_json["results"][result["key"]["dataset"]]["size"] = result["total_size"]["value"]
                    self.generated_json["results"][result["key"]["dataset"]]["datasets"] = result["number_of_datasets"]["value"]
                    self.generated_json["results"][result["key"]["dataset"]]["deposits"] = result["number_of_deposits"]["doc_count"]
                    self.generated_json["results"][result["key"]["dataset"]]["mkdir"] = result["number_of_mkdir"]["doc_count"]
                    self.generated_json["results"][result["key"]["dataset"]]["symlink"] = result["number_of_symlink"]["doc_count"]
                    self.generated_json["results"][result["key"]["dataset"]]["rmdir"] = result["number_of_rmdir"]["doc_count"]
                    self.generated_json["results"][result["key"]["dataset"]]["remove"] = result["number_of_remove"]["doc_count"]

                after_key = response["aggregations"]["group_by"]["after_key"]
                response = self.get_elasticsearch_response(after_key = after_key, deposits=True)
        else:
            response = self.get_elasticsearch_response(deposits=True)
            self.generated_json["totals"] = {}
            self.generated_json["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
            self.generated_json["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
            self.generated_json["totals"]["deposits"] = response["aggregations"]["grand_total_deposits"]["doc_count"]
            self.generated_json["totals"]["mkdir"] = response["aggregations"]["grand_total_mkdir"]["doc_count"]
            self.generated_json["totals"]["symlink"] = response["aggregations"]["grand_total_symlink"]["doc_count"]
            self.generated_json["totals"]["rmdir"] = response["aggregations"]["grand_total_rmdir"]["doc_count"]
            self.generated_json["totals"]["remove"] = response["aggregations"]["grand_total_remove"]["doc_count"]

            self.generated_json["results"] = {}
            for result in response["aggregations"]["group_by"]["buckets"]:
                self.generated_json["results"][result["key"]] = {}
                self.generated_json["results"][result["key"]]["size"] = result["total_size"]["value"]
                self.generated_json["results"][result["key"]]["datasets"] = result["number_of_datasets"]["value"]
                self.generated_json["results"][result["key"]]["deposits"] = result["number_of_deposits"]["doc_count"]
                self.generated_json["results"][result["key"]]["mkdir"] = result["number_of_mkdir"]["doc_count"]
                self.generated_json["results"][result["key"]]["symlink"] = result["number_of_symlink"]["doc_count"]
                self.generated_json["results"][result["key"]]["rmdir"] = result["number_of_rmdir"]["doc_count"]
                self.generated_json["results"][result["key"]]["remove"] = result["number_of_remove"]["doc_count"]
