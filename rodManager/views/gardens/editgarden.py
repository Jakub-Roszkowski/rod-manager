
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rodManager.dir_models.garden import Garden
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="put",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "sector": openapi.Schema(type=openapi.TYPE_STRING),
            "avenue": openapi.Schema(type=openapi.TYPE_STRING),
            "number": openapi.Schema(type=openapi.TYPE_INTEGER),
            "area": openapi.Schema(type=openapi.TYPE_INTEGER),
            "status": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["id", "sector", "avenue", "number", "area", "status"],
    ),
    responses={
        200: openapi.Response(
            description="Garden edited.",
        ),
        400: openapi.Response(
            description="Bad request.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
        403: openapi.Response(
            description="Forbidden.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"error": openapi.Schema(type=openapi.TYPE_STRING)},
            ),
        ),
    }
)
@api_view(["PUT"])
def edit_garden(self, request):
    if "rodManager.manageGardens" not in request.user.get_all_permissions():
        return Response({"error": "You don't have permission to edit gardens."}, status=status.HTTP_403_FORBIDDEN)
    if not request.data["id"]:
            return Response({"error": "Garden ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    if not request.data["sector"] or not request.data["avenue"] or not request.data["number"] or not request.data["area"] or not request.data["status"]:
            return Response({"error": "Sector, avenue, number, area and status are required."}, status=status.HTTP_400_BAD_REQUEST)
    if request.data["status"] not in ["dostępna", "niedostępna"]:
        return Response({"error": "Status must be dostępna or niedostępna."}, status=status.HTTP_400_BAD_REQUEST)
    if not Garden.objects.filter(
        id = request.data["id"],
        sector=request.data["sector"],
        avenue=request.data["avenue"],
        number=request.data["number"],
    ).exists():
        return Response({"error": "Garden doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
    garden = Garden.objects.get(id=request.data["id"])
    garden.leaseholderID = request.data["leaseholderID"]
    garden.status = request.data["status"]
    garden.save()
    return Response({"success": "Garden edited successfully."}, status=status.HTTP_200_OK)