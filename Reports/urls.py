from django.urls import path

from .views import ReportsPage

urlpatterns = [
    path('', ReportsPage.as_view(), name="reports-home")

]