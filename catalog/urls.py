# catalog/urls.py

from django.urls import path, include  
from .views import *

app_name = 'catalog' # Define um namespace para as URLs deste app

urlpatterns = [
    path('part/add/', PartCreateView.as_view(), name='part-add'),
    path('parts/', PartListView.as_view(), name='part-list'),
    path('part/<int:pk>/', PartDetailView.as_view(), name='part-detail'),
    path('project/add/', ProjectCreateView.as_view(), name='project-add'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    
]