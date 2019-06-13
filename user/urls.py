
from django.urls import path

from . import views

urlpatterns = [
    path(r'login/', views.login_view, name='login'),
    path(r'logout/', views.logout_view, name='logout'),
]
