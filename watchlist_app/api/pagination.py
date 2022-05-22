from rest_framework.pagination import PageNumberPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 5
    page_query_param =  'p'
    # it use to go give an access to client to load data as per their requirement
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = 'end'
    