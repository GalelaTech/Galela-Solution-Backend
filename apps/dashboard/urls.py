from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('visits/',   views.VisitsListView.as_view(),   name='visits'),
    path('requests/', views.RequestsListView.as_view(), name='requests'),
    path('requests/<int:pk>/', views.RequestDeleteView.as_view(), name='request-delete'),
    path('visits/<int:pk>/', views.VisitDeleteView.as_view(), name='visit-delete'),
    path('files/<int:pk>/', views.download_file, name='file-download'),
    path('login/', views.login_view, name='login'),
]