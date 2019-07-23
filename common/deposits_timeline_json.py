from common.json_maker import JsonMaker

class DepositsTimelineJson(JsonMaker):
    def get_title(self):
        return "Timeline for deposits to CEDA archive"

    def _populate_json(self):
        response = self.get_elasticsearch_response(deposits=True)
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
        for result in response["aggregations"]["group_by"]["buckets"]:
            if not result["doc_count"]:
                continue
            day = result["key_as_string"]
            self.generated_json["results"][day] = {}
            self.generated_json["results"][day]["size"] = result["total_size"]["value"]
            self.generated_json["results"][day]["datasets"] = result["number_of_datasets"]["value"]
            operations = self.extract_operations(result["total_operations"]["buckets"])
            self.generated_json["results"][day]["deposits"] = operations["deposits"]
            self.generated_json["results"][day]["mkdir"] = operations["mkdir"]
            self.generated_json["results"][day]["symlink"] = operations["symlink"]
            self.generated_json["results"][day]["rmdir"] = operations["rmdir"]
            self.generated_json["results"][day]["remove"] = operations["remove"]

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
