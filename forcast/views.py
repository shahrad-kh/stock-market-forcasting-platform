from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Prediction
from .serializers import PredictionSerializer
from drf_yasg.utils import swagger_auto_schema
import logging

from history.models import Instrument

class PredictionCreateView(APIView):
    @swagger_auto_schema(
        request_body=PredictionSerializer,
        responses={201: PredictionSerializer, 400: "Bad Request"})
    def post(self, request):
        serializer = PredictionSerializer(data=request.data, many=True)

        if serializer.is_valid():
            predictions = [
                Prediction(
                    instrument=Instrument.objects.get(id=item['instrument'].id),
                    date=item['date'],
                    open=item['open'],
                    high=item['high'],
                    low=item['low'],
                    close=item['close'],
                    volume=item['volume']
                )
                for item in serializer.validated_data
            ]
            Prediction.objects.bulk_create(predictions)  # Bulk insert
            logging.info(f"{len(predictions)} prediction data inserted to database.")
            return Response({"message": "Predictions added successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import Prediction
from .serializers import PredictionSerializer

class PredictionByInstrumentView(APIView):
    def get(self, request, instrument_id, days):
        try:
            # Validate input
            days = int(days)
            if days < 0:
                return Response({"error": "Days must be non-negative"}, status=status.HTTP_400_BAD_REQUEST)

            instrument_id = int(instrument_id)
            if instrument_id < 0:
                return Response({"error": "instrument_is must be non-negative"}, status=status.HTTP_400_BAD_REQUEST)

            # Get today's date and calculate the range
            today = datetime.today().date()
            end_date = today + timedelta(days=days)

            # Fetch predictions within the date range
            predictions = Prediction.objects.filter(instrument_id=instrument_id, date__range=[today, end_date])
            
            # Serialize the data
            serializer = PredictionSerializer(predictions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)