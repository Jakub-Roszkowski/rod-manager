from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

employers = [
    {
        'id': 1,
        'position': 'Manager',
        'name': 'John Doe',
        'phoneNumber': '123-456-7890',
        'email': 'john.doe@example.com'
    },
    {
        'id': 2,
        'position': 'Developer',
        'name': 'Jane Smith',
        'phoneNumber': '987-654-3210',
        'email': 'jane.smith@example.com'
    },
    {
        'id': 3,
        'position': 'Designer',
        'name': 'Mike Johnson',
        'phoneNumber': '555-555-5555',
        'email': 'mike.johnson@example.com'
    }
]

class GardenInfoApi(APIView):

    @swagger_auto_schema(
        operation_summary="Get all employers",
        operation_description="Returns a list of all employers.",
        responses={
            200: openapi.Response(
                description="List of all employers",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'position': openapi.Schema(type=openapi.TYPE_STRING),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'phoneNumber': openapi.Schema(type=openapi.TYPE_STRING),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                )
            ),
        },
    )
    def get(self, request):
        return Response(employers)

    @swagger_auto_schema(
        operation_summary="Add a new employer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'position': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'phoneNumber': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={201: "New employer added"},
    )
    def post(self, request):
        new_employer = request.data

        employers.append(new_employer)
        return Response(new_employer, status=status.HTTP_201_CREATED)

class GardenInfoApiWithID(APIView):
    @swagger_auto_schema(
        operation_summary="Update an existing employer",
        manual_parameters=[
            openapi.Parameter('employer_id', openapi.IN_PATH, description="Employer ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'position': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'phoneNumber': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={200: "Employer updated", 404: "Employer not found"},
    )
    def put(self, request, employer_id):
        for employer in employers:
            if employer['id'] == employer_id:
                updated_employer = request.data
                employer.update(updated_employer)
                return Response(employer, status=status.HTTP_200_OK)

        return Response({"error": "Employer not found"}, status=status.HTTP_404_NOT_FOUND)



#     poniej moze byc w properties bez id w put i post
