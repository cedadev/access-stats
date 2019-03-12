from common.json_maker import JsonMaker

class DepositsTimelineJson(JsonMaker):
    def get_title(self):
        return "Timeline for deposits to CEDA archive"

    def _populate_json(self):
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
            if not result["doc_count"]:
                continue
            day = result["key_as_string"]
            self.generated_json["results"][day] = {}
            self.generated_json["results"][day]["size"] = result["total_size"]["value"]
            self.generated_json["results"][day]["datasets"] = result["number_of_datasets"]["value"]
            self.generated_json["results"][day]["deposits"] = result["number_of_deposits"]["doc_count"]
            self.generated_json["results"][day]["mkdir"] = result["number_of_mkdir"]["doc_count"]
            self.generated_json["results"][day]["symlink"] = result["number_of_symlink"]["doc_count"]
            self.generated_json["results"][day]["rmdir"] = result["number_of_rmdir"]["doc_count"]
            self.generated_json["results"][day]["remove"] = result["number_of_remove"]["doc_count"]
