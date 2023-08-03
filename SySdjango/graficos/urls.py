from django.urls import path
from . import views

urlpatterns = [
    path('get_chart/', views.get_chart, name='get_chart'),
]