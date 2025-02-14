from django.urls import path
from .views import PredictionCreateView, PredictionByInstrumentView

urlpatterns = [
    path('CreatePredictions/', PredictionCreateView.as_view(), name='prediction-create'),
    path('GetPredictionsByInstrumentIdAndDays/<int:instrument_id>/<int:days>/', PredictionByInstrumentView.as_view(), name='prediction-by-instrument-and-days'),    
]
