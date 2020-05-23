from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib import admin

urlpatterns = [
    path("", views.analyse, name="analyse"),
    path("result", views.result, name="result"),
    path("job_recom", views.job_recom, name="job_recom"),
    path("recommend", views.recommend, name="recommend"),
    url(r'^jobpost/(?P<id>\d+)/$', views.job_detail, name="job_detail"),
    path('admin/', admin.site.urls),
]