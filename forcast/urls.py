from django.urls import path
from .views import PredictionCreateView

urlpatterns = [
    path('CreatePredictions/', PredictionCreateView.as_view(), name='prediction-create'),
]
