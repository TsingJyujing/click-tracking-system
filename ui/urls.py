from django.urls import path

from . import views

urlpatterns = [
    path(r'search/', views.search_page, name='search'),
    path(r'detail/', views.detail_page, name='detail'),
]
