from common.json_maker import JsonMaker

class UsersJson(JsonMaker):
    def get_title(self):
        return "Summary of downloads from CEDA archive by user"

    def _populate_json(self):
        response = self.get_elasticsearch_response(after_key = 0)
        self.generated_json["totals"] = {}
        self.generated_json["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
        self.generated_json["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
        self.generated_json["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
        self.generated_json["totals"]["accesses"] = 0
        self.generated_json["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
        self.generated_json["totals"]["activitydays"] = self.get_activity_days(response["hits"]["total"])

        self.generated_json["results"] = {}
        while response["aggregations"]["group_by"]["buckets"] != []:
            for result in response["aggregations"]["group_by"]["buckets"]:
                self.generated_json["results"][result["key"]["user"]] = {}

                self.generated_json["results"][result["key"]["user"]]["country"] = result["country"]["buckets"][0]["key"]
                self.generated_json["results"][result["key"]["user"]]["institute_type"] = result["institute_type"]["buckets"][0]["key"]
                self.generated_json["results"][result["key"]["user"]]["field"] = result["field"]["buckets"][0]["key"]

                self.generated_json["results"][result["key"]["user"]]["methods"] = result["number_of_methods"]["value"]
                self.generated_json["results"][result["key"]["user"]]["datasets"] = result["number_of_datasets"]["value"]
                self.generated_json["results"][result["key"]["user"]]["accesses"] = result["number_of_accesses"]["value"]
                self.generated_json["totals"]["accesses"] += result["number_of_accesses"]["value"]
                self.generated_json["results"][result["key"]["user"]]["size"] = result["total_size"]["value"]
                self.generated_json["results"][result["key"]["user"]]["activitydays"] = result["doc_count"]

            after_key = response["aggregations"]["group_by"]["after_key"]
            response = self.get_elasticsearch_response(after_key = after_key)
