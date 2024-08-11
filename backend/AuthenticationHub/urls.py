from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'AuthenticationHub'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('signup/',views.signup_view,name='signup'),
    path('special_signup/',views.staff_signup_view,name='special_signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('signup_seller/',views.seller_signup_view,name='signup_seller'),
    path('login_seller/',views.seller_login_view,name='login_seller'),
    path('forgotpassword/',views.forgot_password,name='forgot_password'),
    path('api/auth/google-signup/', views.google_signup_view, name='google_signup'),
    path('api/auth/google-login/', views.google_login_view, name='google_login'),
    # path('password_save/',views.password_save,name='password_save'),
]
