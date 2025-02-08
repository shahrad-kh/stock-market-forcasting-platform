from rest_framework import serializers
from .models import Instrument, History, RecentUpdate


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ['id', 'name']


class HistorySerializer(serializers.ModelSerializer):
    instrument = InstrumentSerializer(read_only=True)
    instrument_id = serializers.PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(), source='instrument', write_only=True
    )

    class Meta:
        model = History
        fields = ['id', 'instrument', 'instrument_id', 'date', 'open', 'high', 'low', 'close', 'volume']


class RecentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentUpdate
        fields = ['id', 'recent_update_date_time']
