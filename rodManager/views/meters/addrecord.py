
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Meter, Record
from .serializers import RecordSerializer

class AddRecordView(APIView):
    def post(self, request, meter_id):
        try:
            meter = Meter.objects.get(id=meter_id)
        except Meter.DoesNotExist:
            return Response({"error": "Meter not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save(meter=meter)
            return Response(RecordSerializer(record).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
