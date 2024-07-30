from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedImage
from .serializers import UploadedImageSerializer

class ReceiveImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post (self, request, *args, **kwargs) :
        serializer = UploadedImageSerializer(data = request.FILES)

        if serializer.is_valid() :
            serializer.save()

            return Response({"GOOD!"}, status=200)
        else:
            return Response(serializer.errors, status=400)