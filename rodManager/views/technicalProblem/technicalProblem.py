from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



class TechnicalProblem(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'description'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the issue'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the issue'),
            },
        ),
        operation_description="Send an email with the issue title and description."
    )
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')

        if title and description:
            # Tutaj jest symulacja wysłania maila
            # send_mail(
            #     f"Problem: {title}",
            #     f"Opis: {description}",
            #     'sender@example.com',
            #     ['recipient@example.com'],
            #     fail_silently=False,
            # )

            return Response("Mail sent successfully", status=status.HTTP_201_CREATED)
        else:
            return Response("Title and description are required", status=status.HTTP_400_BAD_REQUEST)
