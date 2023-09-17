from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    '''Переопределение пагинации с лимитом. '''
    page_size = 6
    page_size_query_param = 'limit'
