from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.create_request, name='create'),
]