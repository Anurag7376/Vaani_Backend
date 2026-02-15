from django.urls import path
from .views import GovtNewsView

urlpatterns = [
    path('government-news/', GovtNewsView.as_view()),
]
