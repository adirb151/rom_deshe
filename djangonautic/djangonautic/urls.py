from django.contrib import admin
from django.urls import re_path
from django.conf.urls import include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^about$', views.about),
    re_path(r'^$', views.home),
    re_path(r'^queries/', include('queries.urls')),
]

urlpatterns += staticfiles_urlpatterns()
