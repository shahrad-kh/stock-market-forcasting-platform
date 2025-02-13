from django.urls import path

from .views import AllInstrumentsSummaryAPIView, InstrumentHistoryPastDaysView, InstrumentListView, SearchOverInstrumentsSummaryAPIView, AllHistoryInstrumentHistoryByInstrumentIdView

# from .views import CollectHistory


urlpatterns = [
    # path('GetInstrumentHistory/', CollectHistory.as_view(), name='CollectHistory'),
    path('GetAllInstrumentsSummary/<int:page>/', AllInstrumentsSummaryAPIView.as_view(), name='AllInstrumentsSummary'),
    path('SearchOverInstrumentsSummary/<str:instrument_name_query>/<int:page>/', SearchOverInstrumentsSummaryAPIView.as_view(), name='SearchOverInstrumentsSummary'),
    path('GetListOfInstruments/', InstrumentListView.as_view(), name='InstrumentList'),
    path('GetInstrumentHistoryByDay/<int:instrument_id>/<int:days>/', InstrumentHistoryPastDaysView.as_view(), name='InstrumentHistoryPastDays'),
    path('AllHistoryInstrumentHistoryByInstrumentId/<int:instrument_id>/', AllHistoryInstrumentHistoryByInstrumentIdView.as_view(), name='ALLInstrumentHistoryById'),
]
