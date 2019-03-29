from django.urls import path
from django.conf import settings
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path("register", views.register, name = "register"),
    path("logout/", views.logout_request, name = "logout"),
    path("login/", views.login_request, name = "login"),
    path("user/", views.user_page, name = "user"),
    path("lr0-parser/", views.lr0_parser, name = "lr0-parser"),
    path("slr0-parser/", views.slr0_parser, name = "slr0-parser"),
    path("lr1-parser/", views.lr1_parser, name = "lr1-parser"),
    path("lalr1-parser/", views.lalr1_parser, name = "lalr1-parser"),
    path("ll1-parser/", views.ll1_parser, name = "ll1-parser")
]
