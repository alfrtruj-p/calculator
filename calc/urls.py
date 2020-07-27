from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_input, name='data_input'),
    path('quote/<int:pk>/', views.data_quote, name='data_quote'),
    path('quote/<int:pk>/edit/', views.data_edit, name='data_edit'),
    path('quote/history/', views.data_history, name='data_history'),
    ]
