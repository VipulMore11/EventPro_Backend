
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from . import views
# import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('get_userprofile/', views.get_userprofile, name='get_userprofile'),
    path('post_userprofile/', views.post_userprofile, name='post_userprofile'),
]