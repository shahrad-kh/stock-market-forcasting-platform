from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import History, Instrument
from .serializers import HistorySerializer, InstrumentSerializer, InstrumentSummarySerializer
from .services import HistoryRepository, InstrumentRepository

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20


class InstrumentListView(generics.ListAPIView):
    """
    API view to retrieve a list of all instruments.
    """
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    

class AllInstrumentsSummaryAPIView(APIView): 
    pagination_class = CustomPageNumberPagination
    
    def get(self, request, page): 
        
        instrument_ids = InstrumentRepository.get_instrument_ids_with_pagination(self.pagination_class.page_size, page)

        data = HistoryRepository.get_last_history_for_instruments_by_id(instrument_ids)
        
        serializer = InstrumentSummarySerializer(data, many=True)
        return Response(serializer.data, status=200)


class SearchOverInstrumentsSummaryAPIView(APIView): 
    pagination_class = CustomPageNumberPagination

    def get(self, request, instrument_name_query, page): 
        instrument_ids = InstrumentRepository.get_instrument_ids_by_name_query_with_pagination(instrument_name_query, self.pagination_class.page_size, page)
        history = HistoryRepository.get_last_history_for_instruments_by_id(instrument_ids)

        serializer = InstrumentSummarySerializer(history, many=True)
        return Response(serializer.data, status=200)


class InstrumentHistoryPastDaysView(APIView):
    """
    API view to retrieve history records of an instrument within the past specified days.
    Query parameters:
    - instrument_id: ID of the instrument (required)
    - days: Number of past days to filter history records (required)
    example:
    
    """
    
    def get(self, request, instrument_id, days):
        if not instrument_id or not days:
            return Response({"error": "instrument_id and days parameters are required."}, status=400)
        
        try:
            instrument = Instrument.objects.get(id=instrument_id)
        except Instrument.DoesNotExist:
            return Response({"error": "Instrument not found."}, status=404)
        
        try:
            days = int(days)
        except ValueError:
            return Response({"error": "days must be an integer."}, status=400)
        
        histories = History.objects.filter(instrument=instrument).order_by("-date")[:days]
        
        serializer = HistorySerializer(histories, many=True)

        return Response(serializer.data, status=200)


class AllHistoryInstrumentHistoryByInstrumentIdView(APIView):    
    
    def get(self, request, instrument_id):
        if not instrument_id:
            return Response({"error": "instrument_id parameter is required."}, status=400)
        
        try:
            instrument = Instrument.objects.get(id=instrument_id)
        except Instrument.DoesNotExist:
            return Response({"error": "Instrument not found."}, status=404)
                
        histories = History.objects.filter(instrument=instrument).order_by("-date")
        
        serializer = HistorySerializer(histories, many=True)

        return Response(serializer.data, status=200)
