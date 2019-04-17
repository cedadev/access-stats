from common.json_maker import JsonMaker

class DatasetJson(JsonMaker):
    def get_title(self):
        return "Summary of downloads from CEDA archive by dataset"

    def _populate_json(self):
        if self.analysis_method == "dataset":
            response = self.get_elasticsearch_response(after_key = 0)
            activity_days_response = self.get_elasticsearch_response(after_key=0, activity_days=True)
            self.generated_json["totals"] = {}
            self.generated_json["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
            self.generated_json["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
            self.generated_json["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
            self.generated_json["totals"]["accesses"] = response["hits"]["total"]
            self.generated_json["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
            self.generated_json["totals"]["activitydays"] = 0

            self.generated_json["results"] = {}
            while response["aggregations"]["group_by"]["buckets"] != []:
                for result in response["aggregations"]["group_by"]["buckets"]:
                    self.generated_json["results"][result["key"]["dataset"]] = {}
                    self.generated_json["results"][result["key"]["dataset"]]["users"] = result["number_of_users"]["value"]
                    self.generated_json["results"][result["key"]["dataset"]]["methods"] = result["number_of_methods"]["value"]
                    self.generated_json["results"][result["key"]["dataset"]]["accesses"] = result["doc_count"]
                    self.generated_json["results"][result["key"]["dataset"]]["size"] = result["total_size"]["value"]
                    activity_days = self.get_activity_days_scroll(activity_days_response, "dataset", result["key"])
                    self.generated_json["results"][result["key"]["dataset"]]["activitydays"] = activity_days
                    self.generated_json["totals"]["activitydays"] += activity_days

                after_key = response["aggregations"]["group_by"]["after_key"]
                response = self.get_elasticsearch_response(after_key = after_key)
        else:
            response = self.get_elasticsearch_response()
            activity_days_response = self.get_elasticsearch_response(activity_days=True)
            self.generated_json["totals"] = {}
            self.generated_json["totals"]["users"] = response["aggregations"]["grand_total_users"]["value"]
            self.generated_json["totals"]["methods"] = response["aggregations"]["grand_total_methods"]["value"]
            self.generated_json["totals"]["datasets"] = response["aggregations"]["grand_total_datasets"]["value"]
            self.generated_json["totals"]["accesses"] = response["hits"]["total"]
            self.generated_json["totals"]["size"] = response["aggregations"]["grand_total_size"]["value"]
            self.generated_json["totals"]["activitydays"] = activity_days_response["hits"]["total"]

            self.generated_json["results"] = {}
            for result in response["aggregations"]["group_by"]["buckets"]:
                self.generated_json["results"][result["key"]] = {}
                self.generated_json["results"][result["key"]]["users"] = result["number_of_users"]["value"]
                self.generated_json["results"][result["key"]]["methods"] = result["number_of_methods"]["value"]
                self.generated_json["results"][result["key"]]["accesses"] = result["doc_count"]
                self.generated_json["results"][result["key"]]["size"] = result["total_size"]["value"]
                activity_days = self.get_activity_days(activity_days_response, result["key"])
                self.generated_json["results"][result["key"]]["activitydays"] = activity_days
