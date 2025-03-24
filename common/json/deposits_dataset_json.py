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
            operations = self.extract_operations(response["aggregations"]["grand_total_operations"]["buckets"])
            self.generated_json["totals"]["deposits"] = operations["deposits"]
            self.generated_json["totals"]["mkdir"] = operations["mkdir"]
            self.generated_json["totals"]["symlink"] = operations["symlink"]
            self.generated_json["totals"]["rmdir"] = operations["rmdir"]
            self.generated_json["totals"]["remove"] = operations["remove"]

            self.generated_json["results"] = {}
            while response["aggregations"]["group_by"]["buckets"] != []:
                for result in response["aggregations"]["group_by"]["buckets"]:
                    self.generated_json["results"][result["key"]["dataset"]] = {}
                    self.generated_json["results"][result["key"]["dataset"]]["size"] = result["total_size"]["value"]
                    self.generated_json["results"][result["key"]["dataset"]]["datasets"] = result["number_of_datasets"]["value"]
                    operations = self.extract_operations(result["total_operations"]["buckets"])
                    self.generated_json["results"][result["key"]["dataset"]]["deposits"] = operations["deposits"]
                    self.generated_json["results"][result["key"]["dataset"]]["mkdir"] = operations["mkdir"]
                    self.generated_json["results"][result["key"]["dataset"]]["symlink"] = operations["symlink"]
                    self.generated_json["results"][result["key"]["dataset"]]["rmdir"] = operations["rmdir"]
                    self.generated_json["results"][result["key"]["dataset"]]["remove"] = operations["remove"]

                after_key = response["aggregations"]["group_by"]["after_key"]
                response = self.get_elasticsearch_response(after_key = after_key, deposits=True)

    def extract_operations(self, buckets):
        operations = {
            "deposits": 0,
            "mkdir": 0,
            "symlink": 0,
            "rmdir": 0,
            "remove": 0
        }
        for bucket in buckets:
            if bucket["key"] == "DEPOSIT":
                operations["deposits"] = bucket["amount"]["value"]
            elif bucket["key"] == "MKDIR":
                operations["mkdir"] = bucket["amount"]["value"]
            elif bucket["key"] == "SYMLINK":
                operations["symlink"] = bucket["amount"]["value"]
            elif bucket["key"] == "RMDIR":
                operations["rmdir"] = bucket["amount"]["value"]
            elif bucket["key"] == "REMOVE":
                operations["remove"] = bucket["amount"]["value"]
        return operations
