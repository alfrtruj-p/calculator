from django.urls import path
from . import views

urlpatterns = [
    path('quote/input', views.data_input, name='data_input'),
    path('quote/<int:pk>/', views.data_quote, name='data_quote'),
    path('quote/<int:pk>/edit/', views.data_edit, name='data_edit'),
    path('', views.data_history, name='data_history'),
    path('quote/<int:pk>/delete', views.quote_delete, name='quote_delete'),
    ]
