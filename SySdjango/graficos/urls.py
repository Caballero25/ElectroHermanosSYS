from django.urls import path
from . import views

urlpatterns = [
    path('graficos/', views.grafico, name='grafico'),
    path('get_chart/', views.get_chart, name='get_chart')
]