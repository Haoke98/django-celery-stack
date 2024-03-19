"""izBasar URL Configuration

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
import os

from django.conf.urls import include
from django.contrib import admin
from django.contrib.flatpages import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from django.views.static import serve
from revproxy.views import ProxyView
from .view import media
from . import settings
from .settings import STATIC_URL

ADMIN_PATH = os.getenv("ADMIN_PATH")

# 网站标签页名称
admin.site.site_title = _('Django Celery Stack')

# 网站名称：显示在登录页和首页
admin.site.site_header = _('Django Celery Stack | DCS')

admin.autodiscover()
urlpatterns = [
    path(ADMIN_PATH, admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("favicon.ico", RedirectView.as_view(url=STATIC_URL + 'favicon.ico')),
    # path('celery/', include('django_celery_stack.urls')),
    path('sp/', include('simplepro.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, ({'document_root': settings.STATIC_ROOT})),
    re_path(r'^media/(?P<path>.*)$', media),
    re_path(r'^(?P<path>.*)$', ProxyView.as_view(upstream="https://sdc.mldoo.com")),
]
