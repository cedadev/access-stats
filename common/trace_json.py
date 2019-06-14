from common.json_maker import JsonMaker

class TraceJson(JsonMaker):
    def get_title(self):
        return "List of logs within filter"

    def index(self):
        return "main"

    def _populate_json(self):
        response = self.get_elasticsearch_response()
        print(response)
        self.generated_json["logs"] = []
        for result in response["hits"]["hits"]:
            try:
               self.generated_json["logs"].append(f'{result["_source"]["datetime"]},{result["_source"]["method"]},{result["_source"]["filename"]},{result["_source"]["size"]},{result["_source"]["user"]},{result["_source"]["ip"]},{result["_source"]["dataset"]}')
            except KeyError:
                continue
