from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("dashBoard", views.crear_usuarios, name="crear_usuarios"),
    path("account", views.my_account, name="my_account"),
]