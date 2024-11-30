from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.events, name='events'),
    path('calendar/', views.calendar_view, name='calendar'),
]
