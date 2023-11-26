from enum import Enum

from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from rodManager.dir_models.garden import Garden


class TypeOfFee(Enum):
    PerMeter = "Za metr"
    PerGardenPlot = "Za działkę"

class MyGardenAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get garden plot information",
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "sector": openapi.Schema(type=openapi.TYPE_STRING),
                        "avenue": openapi.Schema(type=openapi.TYPE_STRING),
                        "number": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "area": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "leaseholder": openapi.Schema(type=openapi.TYPE_STRING),
                        "value": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "date": openapi.Schema(type=openapi.FORMAT_DATE),
                        "mediaIndividual": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "mediaConsumption": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                        "leaseFees": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_NUMBER),
                                    "sum": openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                        "utilityFees": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_NUMBER),
                                    "sum": openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                        "additionalFees": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "type": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_NUMBER),
                                    "sum": openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                        "individualFees": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "value": openapi.Schema(type=openapi.TYPE_INTEGER),
                                }
                            )
                        ),
                    },
                    required=["sector", "avenue", "number", "area", "leaseholder", "value", "date"]
                )
            ),
            400: openapi.Response(
                description="Invalid request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def get(self, request):
        garden = None
        try:
            garden = Garden.objects.get(id=request.user.id)
        except Garden.DoesNotExist:
            pass
        haveGarden = False

        if (garden != None):
            haveGarden = True

        garden_plot_info = {
            "sector": garden.sector if haveGarden else None,
            "avenue": garden.avenue if haveGarden else None,
            "number": garden.number if haveGarden else None,
            "area": garden.area if haveGarden else None,
            "leaseholder": request.user.first_name + " " + request.user.last_name,
            # TODO: change value to real value from profile
            "value": 3000,
            "date": datetime(2024, 2, 7),
            # TODO: change mediaIndividual to real data from Counters and Payments
            "mediaIndividual": [
                {"name": "Prąd", "mediaConsumption": "10 kW", "value": 200},
                {"name": "Woda", "mediaConsumption": "10 m³", "value": 150},
                {"name": "Razem", "mediaConsumption": None, "value": 350}
            ],
            # TODO: change mediaIndividual to real data from Payments
            "leaseFees": [
                {"name": "PZD", "type": TypeOfFee.PerMeter.value, "value": 0.12, "sum": 200},
                {"name": "Opłata ogrodowa", "type": TypeOfFee.PerMeter.value, "value": 0.61, "sum": 200},
                {"name": "Opłata Inwestycyjna", "type": TypeOfFee.PerMeter.value, "value": 0.5, "sum": 200},
                {"name": "Razem", "type": None, "value": None, "sum": 600}
            ],
            # TODO: change mediaIndividual to real data from Counters and Payments
            "utilityFees": [
                {"name": "Prąd", "type": TypeOfFee.PerMeter.value, "value": 0.12, "sum": 200},
                {"name": "Woda", "type": TypeOfFee.PerMeter.value, "value": 0.61, "sum": 200},
                {"name": "Razem", "type": None, "value": None, "sum": 400}
            ],
            # TODO: change mediaIndividual to real data from Payments
            "additionalFees": [
                {"name": "Koszenie trawy", "type": TypeOfFee.PerGardenPlot.value, "value": 70, "sum": 200},
                {"name": "Grabienie liści", "type": TypeOfFee.PerGardenPlot.value, "value": 40, "sum": 200},
                {"name": "Razem", "type": None, "value": None, "sum": 400}
            ],
            # TODO: change mediaIndividual to real data from individual Payments
            "individualFees": [
                {"name": "Opłata za przekroczenie limitu wody", "value": 40},
                {"name": "Opłata za opiekę nad roślinami w czasie urlopu", "value": 100},
                {"name": "Razem", "value": 140}
            ]
        }

        return Response(garden_plot_info, status=status.HTTP_200_OK)
