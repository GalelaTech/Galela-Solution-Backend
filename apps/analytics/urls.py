from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('visit/', views.track_visit, name='track-visit'),
]