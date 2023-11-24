from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class RODPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 1e20

    def get_paginated_response(self, data):
        return Response({"count": self.page.paginator.count, "results": data})
