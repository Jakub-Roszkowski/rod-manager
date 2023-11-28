from functools import wraps

from rest_framework import status
from rest_framework.response import Response


def permission_required(permissionsList=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print(request.request.user)
            print(permissionsList)
            if request.request.user.is_authenticated:
                if request.request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                if request.request.user.groups.filter(name="ADMIN").exists():
                    return view_func(request, *args, **kwargs)
                if isinstance(permissionsList, str):
                    if request.request.user.has_perm(permissionsList):
                        return view_func(request, *args, **kwargs)
                else:
                    for permission in permissionsList:
                        if request.request.user.has_perm(permission):
                            return view_func(request, *args, **kwargs)
                return Response(
                    {"error": "You do not have permission to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                return Response(
                    {"error": "You must be logged in to perform this action."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return _wrapped_view

    return decorator
