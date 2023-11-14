
from rest_framework import serializers
from rest_framework.views import APIView
from dir_models.meter import Meter
from dir_models.record import Record


class FindMeter(APIView):
    def post(request):
        if "rodManager.manageMeters" not in request.user.get_all_permissions():
            return Response({"error": "You don't have permission to find meters."}, status=status.HTTP_403_FORBIDDEN)
        if request.data["id"]:
            if not Meter.objects.filter(id=request.data["id"]).exists():
                return Response({"error": "Meter doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
            meter = Meter.objects.get(id=request.data["id"])
        elif request.data["address"]:
            if not Meter.objects.filter(address=request.data["address"]).exists():
                return Response({"error": "Meter doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
            meter = Meter.objects.get(address=request.data["address"])
        elif request.data["garden"]:
            if not Meter.objects.filter(garden=request.data["garden"]).exists():
                return Response({"error": "Meter doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
            meter = Meter.objects.get(garden=request.data["garden"])
        else:
            return Response({"error": "ID, address or garden is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = MeterSerializer(meter)
        records = Record.objects.filter(meterID=meter.id)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = '__all__'
        