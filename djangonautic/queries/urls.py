from django.urls import re_path
from . import views

app_name = 'queries'

urlpatterns = [
    re_path(r'^$', views.query_list, name='list'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.query_detail, name='detail')
]
