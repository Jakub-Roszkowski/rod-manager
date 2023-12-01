from datetime import datetime

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.pool import Option, Pool, PoolSerializer, Vote


class CompletedPools(APIView):
    @extend_schema(
        summary="Currents pools",
        description="Get currents pools.",
        responses={200: PoolSerializer(many=True)},
    )
    def get(self, request):
        pools = Pool.objects.filter(end_date__lt=datetime.now())
        serializer = PoolSerializer(pools, many=True)
        return Response(serializer.data)
