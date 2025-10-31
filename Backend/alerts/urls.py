# alerts/urls.py

from django.urls import path
from .views import CreateAlertView, AlertSummariesView

urlpatterns = [
    path('create/', CreateAlertView.as_view(), name='create-alert'),
    path('summaries/', AlertSummariesView.as_view(), name='alert-summaries'),
]