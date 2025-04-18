import csv
from io import StringIO

class QueryBuilder:
    def __init__(self, filters, analysis_method):
        self.filters = filters
        self.analysis_method = analysis_method
        
    def query(self):
        self.generate_query()
        return self.generated_query

    def generate_query(self):
        self.generated_query = self.base_query()
        self.update_filters()
        self.update_aggs()

    def get_size(self):
        return NotImplementedError

    def update_aggs(self):
        return NotImplementedError

    def method(self):
        return "method.keyword.terms.value"

    def datetime(self):
        return "datetime.date_histogram.timestamp"

    def user(self):
        return "user.terms.value"
    
    def dataset(self):
        return "dataset.keyword.terms.value"
    
    def size(self):
        return "size.sum.value"
    
    def country(self):
        return "country.terms.value"
    
    def bots(self):
        bot_list = []

        with open('bot_list.txt', 'r') as fh:
            for line in fh:
                bot_list.append(int(line))
        query_bit = {}

        return query_bit
    
    def must_wildcard_dict_create(self, field, filter_values):
        f = StringIO(filter_values)
        reader = csv.reader(f, delimiter=',')

        for rows in reader:
            filter_val_length = len(rows) - 1
            query_str = ""
            for i, row in enumerate(rows):

                if "dataset.keyword" in field: # need to escape "/" as they are special characters in a query string
                    row = row.replace("/", "\\/")

                if (i == filter_val_length) | (filter_val_length == 0):
                    query_str = query_str + f'*{row}*'
                else:
                    query_str = query_str + f'*{row}*' + " OR "

        self.generated_query["query"]["bool"]["must"].append({
            "query_string": {
                "query": query_str,
                "fields": [field]
            }
        })
    
    def base_query(self):
        return {
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [],
                    "should": [],
                    "filter": {
                        "range": {
                            self.datetime(): {
                                "gte": "2012-01-01",
                                "lte": "now",
                                "format": "yyyy-MM-dd"
                            }
                        }
                    }
                }
            },
            "_source": [],
            "size": self.get_size(),
            "aggs": {}
        }

    def update_filters(self):
        if self.filters["start"]:
            self.generated_query["query"]["bool"]["filter"]["range"][self.datetime()]["gte"] = self.filters["start"]
        if self.filters["end"]:
            self.generated_query["query"]["bool"]["filter"]["range"][self.datetime()]["lte"] = self.filters["end"]
        if "user" in self.filters:
            if self.filters["user"]:
                self.must_wildcard_dict_create(field=self.user(), filter_values= self.filters["user"])


        if self.filters["bots"]:
            ...
            # self.bots()

        if self.filters["dataset"]:
            self.must_wildcard_dict_create(field=self.dataset(), filter_values= self.filters["dataset"])
        if self.filters["method"]:
            self.must_wildcard_dict_create(field=self.method(), filter_values= self.filters["method"])
        if self.filters["anon"]:
            if self.filters["anon"] == "anon":
                self.generated_query["query"]["bool"]["must"].append({
                            "wildcard": {
                                self.user(): {
                                    "value": "anonymous@*"
                                }
                            }
                        })
            if self.filters["anon"] == "non-anon":
                self.generated_query["query"]["bool"]["must_not"].append({
                            "wildcard": {
                                self.user(): {
                                    "value": "anonymous@*"
                                }
                            }
                        })


    # Functions that add aggregations to the generated query:
    # To be called per subclass in update_aggs()
    def grand_totals(self):
        self.generated_query["aggs"].update({
            "grand_total_users": {
                "cardinality": {
                    "field": self.user()
                }
            },
            "grand_total_methods": {
                "cardinality": {
                    "field": self.method()
                }
            },
            "grand_total_datasets": {
                "cardinality": {
                    "field": self.dataset()
                }
            },
            "grand_total_size": {
                "sum": {
                    "field": self.size()
                }
            },
            "grand_total_country": {
                "cardinality": {
                    "field": self.country()
                }
            }
        })
    
    def group_by(self):
        self.generated_aggs = self.base_aggs()
        self.group_by_main()
        self.generated_query["aggs"].update(self.generated_aggs)

    def group_by_main(self):
        return NotImplementedError

    def base_aggs(self):
        return {
            "group_by": {
                "aggs": {
                    "number_of_users": {
                        "cardinality": {
                            "field": self.user()
                        }
                    },
                    "number_of_methods": {
                        "cardinality": {
                            "field": self.method()
                        }
                    },
                    "number_of_datasets": {
                        "cardinality": {
                            "field": self.dataset()
                        }
                    },
                    "number_of_accesses": {
                        "sum": {
                            "field": "method.keyword.terms._count"
                        }
                    },
                    "total_size": {
                        "sum": {
                            "field": self.size()
                        }
                    },
                    "number_of_countries": {
                        "cardinality": {
                            "field": self.country()
                        }
                    }
                }
            }
        }
