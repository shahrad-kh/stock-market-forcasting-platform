from django.urls import path

from .views import CollectHistory


urlpatterns = [
    path('GetInstrumentHistory/', CollectHistory.as_view(), name='CollectHistory'),
]
