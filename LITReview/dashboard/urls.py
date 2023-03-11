from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
]
