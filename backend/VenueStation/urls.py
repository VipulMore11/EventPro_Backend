
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('get_venue/', views.get_venue, name='get_venue'),
    path('post_venue/', views.post_venue, name='post_venue'),
]