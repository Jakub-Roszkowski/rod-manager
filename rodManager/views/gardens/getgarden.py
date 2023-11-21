from rest_framework.decorators import api_view
from rest_framework.response import Response
from dir_models.garden import Garden


@api_view(['GET'])
def garden_in_bulk(request):
    if request.user.is_authenticated:
        gardens = Garden.objects.iterator()[request.GET["index"]:request.GET["index"]+request.GET["size"]]
        return Response(gardens)
    else:
        return Response({"error": "You don't have permission to view gardens."})
                                  
        
    
@api_view(['post'])
def garden_by_id(request):
    if request.user.is_authenticated:
        if Garden.objects.filter(id=request.data["id"]).exists():
            garden = Garden.objects.get(id=request.data["id"])
            return Response(garden)
        else:
            return Response({"error": "Garden doesn't exist."})
    else:
        return Response({"error": "You don't have permission to view gardens."})