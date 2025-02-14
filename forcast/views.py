from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Prediction
from .serializers import PredictionSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class PredictionCreateView(APIView):
    @swagger_auto_schema(
        request_body=PredictionSerializer,
        responses={201: PredictionSerializer, 400: "Bad Request"})
    def post(self, request):
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
