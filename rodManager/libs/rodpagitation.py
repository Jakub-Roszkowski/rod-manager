from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class RODPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 1e20

    def get_paginated_response(self, data):
        return Response({"count": self.page.paginator.count, "results": data})

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'results': schema,
        }
        }