from rest_framework import serializers
from .models import Instrument, History


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['id', 'name']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'instrument_id', 'date', 'open', 'high', 'low', 'volume', 'close']


class InstrumentSummarySerializer(serializers.Serializer):
    InstrumentId = serializers.IntegerField()
    InstrumentName = serializers.CharField()
    HistoryId = serializers.IntegerField()
    Date = serializers.DateField(format="%Y-%m-%d") 
    Close = serializers.IntegerField()
    Open = serializers.IntegerField()
    High = serializers.IntegerField()
    Low = serializers.IntegerField()
    Volume = serializers.IntegerField()
    Change = serializers.FloatField()