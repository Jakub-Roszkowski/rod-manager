from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.libs.rodpagitation import RODPagination
from rodManager.dir_models.employee import Employee

employees = [
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

class RODInfoApi(APIView):

    @swagger_auto_schema(
        operation_summary="Get all employees",
        operation_description="Returns a list of all employees.",
        responses={
            200: openapi.Response(
                description="List of all employees",
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
        pagination_class = RODPagination
        paginator = RODPagination()

        employees = paginator.paginate_queryset(Employee.objects.all(), request)
        return paginator.get_paginated_response(employees)
        

    @swagger_auto_schema(
        operation_summary="Add a new employee",
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
        responses={201: "New employee added"},
    )
    def post(self, request):
        new_employee = request.data
        if not new_employee["position"]:
            return Response({"error": "Position is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not new_employee["name"]:
            return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not new_employee["phoneNumber"]:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not new_employee["email"]:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        Employee.objects.create(**new_employee)
        return Response(new_employee, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Update an existing employee",
        manual_parameters=[
            openapi.Parameter('employee_id', openapi.IN_PATH, description="employee ID", type=openapi.TYPE_INTEGER)
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
        responses={200: "employee updated", 404: "employee not found"},
    )
    def put(self, request, employee_id):
        new_employee = request.data
        if not Employee.objects.filter(id=employee_id).exists():
            return Response({"error": "employee not found"}, status=status.HTTP_404_NOT_FOUND)
        employee = Employee.objects.get(id=employee_id)
        if new_employee["position"]:
            employee.position = new_employee["position"]
        if new_employee["name"]:
            employee.name = new_employee["name"]
        if new_employee["phoneNumber"]:
            employee.phoneNumber = new_employee["phoneNumber"]
        if new_employee["email"]:
            employee.email = new_employee["email"]
        employee.save()
        return Response(new_employee, status=status.HTTP_200_OK)




#     poniej moze byc w properties bez id w put i post
