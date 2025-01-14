from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.my_view, name='my_view'),
]
