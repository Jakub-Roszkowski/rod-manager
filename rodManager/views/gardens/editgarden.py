
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dir_models.garden import Garden

class EditGardenView(APIView):

    def put(self, request):
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