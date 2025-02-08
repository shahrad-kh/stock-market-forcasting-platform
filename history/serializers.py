from rest_framework import serializers
from .models import Instrument, History, RecentUpdate

# Serializers
class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class RecentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentUpdate
        fields = '__all__'