from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from dir_models.meter import Meter

@api_view(['POST'])
def add_meter(request):
    serializer = MeterSerializer(data=request.data)
    if "rodManager.manageMeters" not in request.user.get_all_permissions():
        return Response({"error": "You don't have permission to add meters."}, status=status.HTTP_403_FORBIDDEN)
    if (not request.data["address"] and not request.data["garden"]) or not request.data["type"]:
        return Response({"error": "Address or garden,  and type are required."}, status=status.HTTP_400_BAD_REQUEST)
    serializer.is_valid(raise_exception=True)
    meter = Meter.objects.create(
        address=request.data["address"],
        garden=request.data["garden"],
        type=request.data["type"],
    )
class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = '__all__'