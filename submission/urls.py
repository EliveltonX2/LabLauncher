# submission/urls.py
from django.urls import path
from .views import curation_queue_view

app_name = 'submission'

urlpatterns = [
    path('', curation_queue_view, name='curation-queue'),
]