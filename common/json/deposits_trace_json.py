from common.json.trace_json import TraceJson

class DepositsTraceJson(TraceJson):
    def _populate_json(self):
        response = self.get_elasticsearch_response(deposits=True)
        self.generated_json["logs"] = []
        for result in response["hits"]["hits"]:
            try:
               self.generated_json["logs"].append(f'{result["_source"]["datetime"]},{result["_source"]["operation"]},{result["_source"]["filename"]},{result["_source"]["size"]},{result["_source"]["dataset"]}')
            except KeyError:
                continue
