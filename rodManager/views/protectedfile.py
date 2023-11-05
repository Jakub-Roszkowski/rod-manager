from django.http import HttpResponse
from django.views import View


class ProtectedFileView(View):
    def get(self, request, file_id):
        response = HttpResponse()
        response["X-Accel-Redirect"] = f"/media/{file_id}"
        return response
