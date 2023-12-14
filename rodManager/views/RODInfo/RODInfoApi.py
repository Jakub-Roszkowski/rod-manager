from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rodManager.libs.rodpagitation import RODPagination
from rodManager.dir_models.employee import Employee, EmployeeSerializer

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

    @extend_schema(
        summary="Get employees",
        description="Get all employees.",
        parameters=[
            OpenApiParameter(name="page", type=OpenApiTypes.INT),
            OpenApiParameter(name="page_size", type=OpenApiTypes.INT),
        ],
        responses={
            200: OpenApiResponse(
                description="Employee list.",
                response=Employee,
            ),
        }
    )
    def get(self, request):
        return Response(EmployeeSerializer(Employee.objects.all(), many=True).data, status=status.HTTP_200_OK)
        

    @extend_schema(
        summary="Create employee",
        request=Employee,
        responses={
            200: OpenApiResponse(
                description="Employee created.",
                response=Employee,
            ),
        }
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

    @extend_schema(
        summary="Edit employee",
        parameters=[
            OpenApiParameter(
                name="employee_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="employee_id",
            ),
        ],
        request=Employee,
        responses={
            200: OpenApiResponse(
                description="Employee edited.",
                response=Employee,
            ),
        }
    )


    def put(self, request):
        employee_id = request.query_params.get("employee_id")

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
    
    def delete(self, request, employee_id):
        if not Employee.objects.filter(id=employee_id).exists():
            return Response({"error": "employee not found"}, status=status.HTTP_404_NOT_FOUND)
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        return Response(status=status.HTTP_200_OK)




#     poniej moze byc w properties bez id w put i post
