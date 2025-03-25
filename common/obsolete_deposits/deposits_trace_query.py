from common.obsolete_deposits.deposits_query_builder import DepositsQueryBuilder
from common.es_queries.trace_query import TraceQuery

class DepositsTraceQuery(TraceQuery, DepositsQueryBuilder):
    pass
