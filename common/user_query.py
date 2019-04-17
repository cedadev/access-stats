from common.query_builder import QueryBuilder

class UserQuery(QueryBuilder):
    def get_size(self):
        return 0

    def update_aggs(self):
        self.group_by()

    def group_by_main(self):
        self.generated_aggs["group_by_field"] = {}
        self.generated_aggs["group_by_field"]["terms"] = {}
        self.generated_aggs["group_by_field"]["terms"]["field"] = "user_data.field.keyword"
        self.generated_aggs["group_by_field"]["aggs"] = {}
        self.generated_aggs["group_by_field"]["aggs"]["users"] = {}
        self.generated_aggs["group_by_field"]["aggs"]["users"]["cardinality"] = {}
        self.generated_aggs["group_by_field"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

        self.generated_aggs["group_by_country"] = {}
        self.generated_aggs["group_by_country"]["terms"] = {}
        self.generated_aggs["group_by_country"]["terms"]["field"] = "user_data.isocode.keyword"
        self.generated_aggs["group_by_country"]["aggs"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"]["cardinality"] = {}
        self.generated_aggs["group_by_country"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

        self.generated_aggs["group_by_institute_type"] = {}
        self.generated_aggs["group_by_institute_type"]["terms"] = {}
        self.generated_aggs["group_by_institute_type"]["terms"]["field"] = "user_data.type.keyword"
        self.generated_aggs["group_by_institute_type"]["aggs"] = {}
        self.generated_aggs["group_by_institute_type"]["aggs"]["users"] = {}
        self.generated_aggs["group_by_institute_type"]["aggs"]["users"]["cardinality"] = {}
        self.generated_aggs["group_by_institute_type"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

        self.generated_aggs["group_by_oda_type"] = {}
        self.generated_aggs["group_by_oda_type"]["terms"] = {}
        self.generated_aggs["group_by_oda_type"]["terms"]["field"] = "user_data.oda_country.keyword"
        self.generated_aggs["group_by_oda_type"]["aggs"] = {}
        self.generated_aggs["group_by_oda_type"]["aggs"]["users"] = {}
        self.generated_aggs["group_by_oda_type"]["aggs"]["users"]["cardinality"] = {}
        self.generated_aggs["group_by_oda_type"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

        self.generated_aggs["group_by_area"] = {}
        self.generated_aggs["group_by_area"]["terms"] = {}
        self.generated_aggs["group_by_area"]["terms"]["field"] = "user_data.area.keyword"
        self.generated_aggs["group_by_area"]["aggs"] = {}
        self.generated_aggs["group_by_area"]["aggs"]["users"] = {}
        self.generated_aggs["group_by_area"]["aggs"]["users"]["cardinality"] = {}
        self.generated_aggs["group_by_area"]["aggs"]["users"]["cardinality"]["field"] = "user.keyword"

    def base_aggs(self):
        return {}