from django.urls import path

from core_app import views

app_name = "core_app"

urlpatterns = [
    path(
        "create/",
        views.CreateUserView.as_view(),
        name="create"
    ),

    path(
        "login/",
        views.CreateTokeView.as_view(),
        name="token"
    ),

    path(
        "me/",
        views.ManageUserView.as_view(),
        name="me"
    ),
]
