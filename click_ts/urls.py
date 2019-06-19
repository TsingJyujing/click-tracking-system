"""click_ts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from api.views import get_redirect_page

urlpatterns = [
    path(r'j/', get_redirect_page),
    path(r'api/', include('api.urls')),
    # todo 等待页面开发完成再开放
    # path(r'ui/', include('ui.urls')),
    # path(r'admin/', admin.site.urls),
    # path(r'users/', include('user.urls')),
    # path(r'users/', include('django.contrib.auth.urls')),
    # path(r'static/', static.serve, {'document_root': settings.STATIC_ROOT}, name='static')
]
