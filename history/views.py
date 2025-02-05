from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import History, Instrument, RecentUpdate
from .serializers import (HistorySerializer, InstrumentSerializer,
                          RecentUpdateSerializer)


# custom pagination class
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 15


class InstrumentListView(generics.ListAPIView):
    """
    API view to retrieve a list of all instruments.
    """
    
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    pagination_class = CustomPageNumberPagination  # Add pagination to this view


class InstrumentRetrieveView(generics.RetrieveAPIView):
    """
    API view to retrieve a single instrument by ID.
    """
    
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer


class HistoryListView(generics.ListAPIView):
    """
    API view to retrieve a list of all history records.
    """
    
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    pagination_class = CustomPageNumberPagination  # Add pagination to this view


class HistoryRetrieveView(generics.RetrieveAPIView):
    """
    API view to retrieve a single history record by ID.
    """
    
    queryset = History.objects.all()
    serializer_class = HistorySerializer


class RecentUpdateListView(generics.ListAPIView):
    """
    API view to retrieve a list of all recent updates.
    """
    
    queryset = RecentUpdate.objects.all()
    serializer_class = RecentUpdateSerializer
    pagination_class = CustomPageNumberPagination  # Add pagination to this view


class RecentUpdateRetrieveView(generics.RetrieveAPIView):
    """
    API view to retrieve a single recent update by ID.
    """
    
    queryset = RecentUpdate.objects.all()
    serializer_class = RecentUpdateSerializer
    

class InstrumentHistoryPastDaysView(APIView):
    """
    API view to retrieve history records of an instrument within the past specified days.
    Query parameters:
    - instrument_id: ID of the instrument (required)
    - days: Number of past days to filter history records (required)
    example: 
    """
    
    def get(self, request):
        instrument_id = request.query_params.get('instrument_id')
        days = request.query_params.get('days')
        
        if not instrument_id or not days:
            return Response({"error": "instrument_id and days query parameters are required."}, status=400)
        
        try:
            instrument = Instrument.objects.get(id=instrument_id)
        except Instrument.DoesNotExist:
            return Response({"error": "Instrument not found."}, status=404)
        
        try:
            days = int(days)
        except ValueError:
            return Response({"error": "days must be an integer."}, status=400)
        
        start_date = date.today() - timedelta(days=days)
        histories = History.objects.filter(instrument=instrument, date__gte=start_date)
        
        # Apply pagination manually for this view
        paginator = CustomPageNumberPagination()
        paginated_histories = paginator.paginate_queryset(histories, request)
        serializer = HistorySerializer(paginated_histories, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
