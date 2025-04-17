from common.json_maker import JsonMaker

class UserJson(JsonMaker):
    def get_title(self):
        return "User breakdown of downloads from CEDA archive"

    def _populate_json(self):
        response = self.get_elasticsearch_response(after_key = 0)

        users_total = 0
        countries_total = 0

        self.generated_json["results"] = {}
        for grouping in response["aggregations"]:
            self.generated_json["results"][grouping] = {}
            for result in response["aggregations"][grouping]["buckets"]:
                self.generated_json["results"][grouping][result["key"]] = result["users"]["value"]

                countries_total = countries_total + 1
                users_total = users_total + result["users"]["value"]

        self.generated_json["totals"] = {}
        self.generated_json["totals"]["countries"] = countries_total
        self.generated_json["totals"]["users"] = users_total
