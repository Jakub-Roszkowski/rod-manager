from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rodManager.dir_models.rod_gardens import RODGardens

RODDescription = "Rodzinny Ogród Działkowy we Wrocławiu jest oazą zieleni i spokoju w sercu miasta. Został założony ponad 50 lat temu i od tego czasu stanowi nie tylko miejsce uprawy roślin, ale także centrum społeczności ogrodniczej.\n" + "\n" + "Na obszarze ROD znajduje się blisko sto działek, każda z własnym charakterem i osobistym podejściem do ogrodnictwa. Jest to miejsce, gdzie ludzie o różnych doświadczeniach ogrodniczych spotykają się, dzieląc się wiedzą i wzajemnie inspirując do nowych pomysłów.\n" + "\n" + "Wśród działek znajdują się różnorodne ogrody - od tych pełnych kolorowych kwiatów, przez ogródki warzywne, po miejsca pełne egzotycznych roślin. Ale nie tylko rośliny są tu ważne. Altanki, małe ławeczki, czy nawet małe domki dla narzędzi to często spotykane elementy, które nadają charakter poszczególnym działkom.\n" + "\n" + "W ROD we Wrocławiu istnieje swoisty rytm życia. Rankiem można spotkać ogrodników, którzy przychodzą, aby sprawdzić stan swoich upraw, podlać kwiaty czy zebrać świeże warzywa na dzisiejszy obiad. Wieczory są czasem na spacery po alejkach wśród zapachów kwiatów i odgłosów natury.\n" + "\n" + "Społeczność ROD jest wyjątkowo zżyta. Organizowane są tu różnorodne wydarzenia - od wspólnych pikników, przez konkursy na najpiękniejsze ogródki, po warsztaty ogrodnicze dla najmłodszych. To miejsce, gdzie sąsiedzi nie tylko pomagają sobie nawzajem, ale także tworzą silne więzi i przyjaźnie.\n" + "\n" + "Rodzinny Ogród Działkowy we Wrocławiu to nie tylko zbiór działek, to miejsce, gdzie rośnie coś więcej niż tylko rośliny - rozwija się tu społeczność, wzajemna pomoc i pasja do ogrodnictwa."


class RODInfoDescriptionApi(APIView):
    @swagger_auto_schema(
        operation_summary="Get ROD Description",
        operation_description="Returns a ROD Description",
        responses={
            200: openapi.Response(
                description="List of all employers",
                schema=openapi.Schema(
                    type=openapi.TYPE_STRING,
                )
            ),
        },
    )
    def get(self, request):
        return Response(RODGardens.objects.first().RODDescription)

    @swagger_auto_schema(
        operation_summary="Add a new ROD Description",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING, ),
    )
    def put(self, request):
        new_description = request.data.get('description', None)
        if new_description:
            RODGardens.objects.first().RODDescription = new_description
            return Response("ROD Description updated successfully", status=status.HTTP_200_OK)
        else:
            return Response("No new description provided", status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request):
        RODGardens.objects.create(RODDescription="")
        return Response("ROD Description created successfully", status=status.HTTP_201_CREATED)
