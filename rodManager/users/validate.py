from rest_framework.response import Response
from rest_framework import status


def validateUser(request, public, permissionsList):
    if public:
        return None
    if request.user.is_authenticated == True:
        if request.user.is_superuser:
            return None
        if request.user.groups.filter(name="ADMIN").exists():
            return None
        for permission in permissionsList:
            if not request.user.has_perm(permission):
                return Response(
                    {"error": "You do not have permission to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        return Response(
            {"error": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )
    else:
        return Response(
            {"error": "You must be logged in to perform this action."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
