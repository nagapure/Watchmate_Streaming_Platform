from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 5
    page_query_param =  'p'
    # it use to go give an access to client to load data as per their requirement
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = 'end'
    
class WatchlistLOPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'
    max_limit = 10