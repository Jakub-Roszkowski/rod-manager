from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def permission_required(permissionsList=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.request.user.is_authenticated:
                if request.request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                if request.request.user.groups.filter(name="ADMIN").exists():
                    return view_func(request, *args, **kwargs)
                if isinstance(permissionsList, str):
                    if not request.request.user.has_perm(permissionsList):
                        return Response(
                            {
                                "error": "You do not have permission to perform this action."
                            },
                            status=status.HTTP_403_FORBIDDEN,
                        )
                else:
                    for permission in permissionsList:
                        if not request.request.user.has_perm(permission):
                            return Response(
                                {
                                    "error": "You do not have permission to perform this action."
                                },
                                status=status.HTTP_403_FORBIDDEN,
                            )
                return view_func(request, *args, **kwargs)
            else:
                return Response(
                    {"error": "You must be logged in to perform this action."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return _wrapped_view

    return decorator
