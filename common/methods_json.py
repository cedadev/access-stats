from common.json_maker import JsonMaker

class MethodsJson(JsonMaker):
    def get_title(self):
        return "Summary of downloads from CEDA archive by method"

    def _populate_json(self):
        response = self.get_elasticsearch_response()
        self.generated_json["totals"] = {}
        self.generated_json["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        self.generated_json["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        self.generated_json["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        self.generated_json["totals"]["accesses"] = response["hits"]["total"]
        self.generated_json["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        self.generated_json["totals"]["activitydays"] = response["aggregations"]["grand_total_activitydays"]["value"]

        self.generated_json["results"] = {}
        for result in response["aggregations"]["group_by"]["buckets"]:
            self.generated_json["results"][result["key"]] = {}
            self.generated_json["results"][result["key"]]["users"] = result["number_of_users"]["value"]
            self.generated_json["results"][result["key"]]["datasets"] = result["number_of_datasets"]["value"]
            self.generated_json["results"][result["key"]]["accesses"] = result["doc_count"]
            self.generated_json["results"][result["key"]]["size"] = result["total_size"]["value"]
            self.generated_json["results"][result["key"]]["activitydays"] = result["group_by_activitydays"]["value"]