import os
from django.conf import settings
from account.serializers import ImageUploadForm, FileUploadForm
from utils.shortcuts import rand_str
from utils.api import CSRFExemptAPIView
import logging

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

logger = logging.getLogger(__name__)


class SimditorImageUploadAPIView(CSRFExemptAPIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="image", in_=openapi.IN_FORM, type=openapi.TYPE_FILE
            ),
        ],
    )
    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data["image"]
        else:
            return self.error("Upload failed")

        suffix = os.path.splitext(img.name)[-1].lower()
        if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.error("Unsupported file format")
        img_name = rand_str(10) + suffix
        try:
            with open(os.path.join(settings.UPLOAD_DIR, img_name), "wb") as imgFile:
                for chunk in img:
                    imgFile.write(chunk)
        except IOError as e:
            logger.error(e)
            return self.error("Upload Error")
        return self.success({"file_path": f"{settings.UPLOAD_PREFIX}/{img_name}",
                             "img_name": img_name})


class SimditorFileUploadAPIView(CSRFExemptAPIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="file", in_=openapi.IN_FORM, type=openapi.TYPE_FILE
            ),
        ],
    )
    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
        else:
            return self.error("Upload failed")

        suffix = os.path.splitext(file.name)[-1].lower()
        file_name = rand_str(10) + suffix
        try:
            with open(os.path.join(settings.UPLOAD_DIR, file_name), "wb") as f:
                for chunk in file:
                    f.write(chunk)
        except IOError as e:
            logger.error(e)
            return self.error("Upload Error")
        return self.success({
            "file_path": f"{settings.UPLOAD_PREFIX}/{file_name}",
            "file_name": file.name
        })
