from common.json_maker import JsonMaker

class UsersJson(JsonMaker):
    def get_title(self):
        return "Summary of downloads from CEDA archive by user"

    def _populate_json(self):
        if self.analysis_method == "users":
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
                    self.generated_json["results"][result["key"]["user"]] = {}
                    if result["country"]["buckets"]:
                        if result["key"]["user"].startswith("anonymous@"):
                            self.generated_json["results"][result["key"]["user"]]["country"] = result["country"]["buckets"][0]["key"]
                            self.generated_json["results"][result["key"]["user"]]["institute_type"] = "-"
                            self.generated_json["results"][result["key"]["user"]]["field"] = "-"
                        else:
                            self.generated_json["results"][result["key"]["user"]]["country"] = result["country"]["buckets"][0]["key"]
                            self.generated_json["results"][result["key"]["user"]]["institute_type"] = result["institute_type"]["buckets"][0]["key"]
                            self.generated_json["results"][result["key"]["user"]]["field"] = result["field"]["buckets"][0]["key"]
                    else:
                        self.generated_json["results"][result["key"]["user"]]["country"] = "-"
                        self.generated_json["results"][result["key"]["user"]]["institute_type"] = "-"
                        self.generated_json["results"][result["key"]["user"]]["field"] = "-"

                    self.generated_json["results"][result["key"]["user"]]["methods"] = result["number_of_methods"]["value"]
                    self.generated_json["results"][result["key"]["user"]]["datasets"] = result["number_of_datasets"]["value"]
                    self.generated_json["results"][result["key"]["user"]]["accesses"] = result["doc_count"]
                    self.generated_json["results"][result["key"]["user"]]["size"] = result["total_size"]["value"]
                    activity_days = self.get_activity_days_scroll(activity_days_response, "user", result["key"])
                    self.generated_json["results"][result["key"]["user"]]["activitydays"] = activity_days
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
                if result["country"]["buckets"]:
                    if result["key"].startswith("anonymous@"):
                        self.generated_json["results"][result["key"]]["country"] = result["country"]["buckets"][0]["key"]
                        self.generated_json["results"][result["key"]]["institute_type"] = "-"
                        self.generated_json["results"][result["key"]]["field"] = "-"
                    else:
                        self.generated_json["results"][result["key"]]["country"] = result["country"]["buckets"][0]["key"]
                        self.generated_json["results"][result["key"]]["institute_type"] = result["institute_type"]["buckets"][0]["key"]
                        self.generated_json["results"][result["key"]]["field"] = result["field"]["buckets"][0]["key"]
                else:
                    self.generated_json["results"][result["key"]]["country"] = "-"
                    self.generated_json["results"][result["key"]]["institute_type"] = "-"
                    self.generated_json["results"][result["key"]]["field"] = "-"
                self.generated_json["results"][result["key"]]["methods"] = result["number_of_methods"]["value"]
                self.generated_json["results"][result["key"]]["datasets"] = result["number_of_datasets"]["value"]
                self.generated_json["results"][result["key"]]["accesses"] = result["doc_count"]
                self.generated_json["results"][result["key"]]["size"] = result["total_size"]["value"]
                activity_days = self.get_activity_days(activity_days_response, result["key"])
                self.generated_json["results"][result["key"]]["activitydays"] = activity_days
