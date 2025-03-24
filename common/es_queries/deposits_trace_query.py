from common.es_queries.deposits_query_builder import DepositsQueryBuilder
from common.es_queries.trace_query import TraceQuery

class DepositsTraceQuery(TraceQuery, DepositsQueryBuilder):
    pass
