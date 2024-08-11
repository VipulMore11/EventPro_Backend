from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('new_role/', views.add_role, name="new_role"),
]