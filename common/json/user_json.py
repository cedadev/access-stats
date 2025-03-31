from common.json_maker import JsonMaker

class UserJson(JsonMaker):
    def get_title(self):
        return "User breakdown of downloads from CEDA archive"

    def _populate_json(self):
        response = self.get_elasticsearch_response()
        self.generated_json["results"] = {}
        for grouping in response["aggregations"]:
            self.generated_json["results"][grouping] = {}
            for result in response["aggregations"][grouping]["buckets"]:
                self.generated_json["results"][grouping][result["key"]] = result["users"]["value"]
