
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dir_models.garden import Garden

class DeleteGardenView(APIView):
    def delete(self, request):
        if "rodManager.manageGardens" not in request.user.get_all_permissions():
            return Response({"error": "You don't have permission to delete gardens."}, status=status.HTTP_403_FORBIDDEN)
        if Garden.objects.filter(id=request.data["id"]).exists():
            Garden.objects.get(id=request.data["id"]).delete()
            return Response({"success": "Garden deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Garden doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)