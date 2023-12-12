from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.dir_models.roddocument import RodDocument


class RodDocumentByIdView(APIView):
    @extend_schema(
        summary="Delete system document",
        description="Delete system document by id.",
        responses={204: None},
    )
    def delete(self, request, document_id):
        document = RodDocument.objects.get(pk=document_id)
        document.delete()
        return Response(status=204)
