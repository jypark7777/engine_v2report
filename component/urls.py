from report.views.report import RequestReportComponent
from django.urls import path
from component.views import RequestUserTag

urlpatterns = [
    path('tag/<username>/', RequestUserTag.as_view(), name='usertag')
]
