from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rodManager.dir_models.image import Image
from PIL import Image as PILImage


class ImageView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_FILE),
        responses={
            status.HTTP_201_CREATED: openapi.Response("Image uploaded successfully"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Error uploading image"),
        },
    )
    def post(self, request):
        if request.FILES.get("image"):
            image = request.FILES["image"]
            name = image.name
            try:
                with PILImage.open(image) as img:
                    file = Image(name=name, image=image)
                    file.save()
                    return Response(status=status.HTTP_201_CREATED)
            except PILImage.UnidentifiedImageError:
                return Response(
                    {"error": "Sended file is not a image"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
