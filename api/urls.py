from django.urls import path

from . import views

urlpatterns = [
    path(r'redirect/', views.get_redirect_page, name='redirect'),
    path(r'create/', views.create_new_link, name='create'),
    path(r'disable/', views.disable_link, name='disable'),
    path(r'enable/', views.enable_link, name='enable'),
    path(r'detail/', views.basic_information, name='detail'),
]
