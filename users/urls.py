# users/urls.py
from django.urls import path
from .views import profile_update_view, public_profile_view


app_name = 'users'

urlpatterns = [
    path('profile/', profile_update_view, name='profile'),
    path('<str:username>/', public_profile_view, name='public-profile'),
]