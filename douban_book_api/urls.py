from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("book_api_stats.urls")),
    re_path(r'^static/(?P<path>.*)$', serve),
]