from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.libs.mailsending import send_mail_from_template


class TechnicalProblemSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class TechnicalProblem(APIView):
    @extend_schema(
        summary="Send technical problem",
        description="Send technical problem.",
        request=TechnicalProblemSerializer,
        responses={201: None},
    )
    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")

        if title and description:
            data = {
                "imie_nazwisko": request.user.first_name + " " + request.user.last_name,
                "email": request.user.email,
                "temat_problemu": title,
                "opis_problemu": description,
            }
            if (
                send_mail_from_template(
                    "technical_problem",
                    "Problem techniczny",
                    ["tomik12124@gmail.com", "tomek@plociennik.info", "roszkolgaming@gmail.com"],
                    data,
                )
                == "error"
            ):
                return Response(
                    "Mail not sent", status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response("Mail sent successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(
                "Title and description are required", status=status.HTTP_400_BAD_REQUEST
            )
