from common.json_maker import JsonMaker

class TimelineJson(JsonMaker):
    def get_title(self):
        return "Timeline for downloads from CEDA archive"

    def _populate_json(self):
        response = self.get_elasticsearch_response()
        self.generated_json["totals"] = {}
        self.generated_json["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        self.generated_json["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        self.generated_json["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        self.generated_json["totals"]["accesses"] = 0
        self.generated_json["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        self.generated_json["totals"]["countries"] = response["aggregations"]["grand_total_country"]["value"]
        self.generated_json["totals"]["activitydays"] = self.get_activity_days(response["hits"]["total"])

        self.generated_json["results"] = {}
        for result in response["aggregations"]["group_by"]["buckets"]:
            month = result["key_as_string"]
            self.generated_json["results"][month] = {}
            self.generated_json["results"][month]["users"] = result["number_of_users"]["value"]
            self.generated_json["results"][month]["methods"] = result["number_of_methods"]["value"]
            self.generated_json["results"][month]["datasets"] = result["number_of_datasets"]["value"]
            self.generated_json["results"][month]["accesses"] = result["number_of_accesses"]["value"]
            self.generated_json["totals"]["accesses"] += result["number_of_accesses"]["value"]
            self.generated_json["results"][month]["size"] = result["total_size"]["value"]
            self.generated_json["results"][month]["countries"] = result["number_of_countries"]["value"]
            self.generated_json["results"][month]["activitydays"] = result["doc_count"]
