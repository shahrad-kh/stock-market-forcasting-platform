from django.urls import path

from .views import (HistoryListView, HistoryRetrieveView,
                    InstrumentHistoryPastDaysView, InstrumentListView,
                    InstrumentRetrieveView, RecentUpdateListView,
                    RecentUpdateRetrieveView)

# from .views import CollectHistory


urlpatterns = [
    # path('GetInstrumentHistory/', CollectHistory.as_view(), name='CollectHistory'),
    
    path('GetListOfInstruments/', InstrumentListView.as_view(), name='instrument-list'),
    path('GetDetailOfInstrumentsByID/<int:pk>/', InstrumentRetrieveView.as_view(), name='instrument-detail'),
    
    path('GetListOfHistory/', HistoryListView.as_view(), name='history-list'),
    path('GetDetailOfHistoryByID/<int:pk>/', HistoryRetrieveView.as_view(), name='history-detail'),
    
    path('GetListOfRecentUpdates/', RecentUpdateListView.as_view(), name='recent-update-list'),
    path('GetDetailOfRecentUpdatesByID/<int:pk>/', RecentUpdateRetrieveView.as_view(), name='recent-update-detail'),

    path('GetInstrumentHistoryByDay/', InstrumentHistoryPastDaysView.as_view(), name='instrument-history-past-days'),
]
