from django.urls import path
from django.conf import settings
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path("register", views.register, name = "register"),
    path("logout/", views.logout_request, name = "logout"),
    path("login/", views.login_request, name = "login"),
    path("user/", views.user_page, name = "user")
]
