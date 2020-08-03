from django.urls import path

from .views import TaskAPIView, TaskRetrieveUpdateAPIView, TaskAcceptAPIView

app_name = "task_app"

urlpatterns = [
    path(
        "task/",
        TaskAPIView.as_view(),
        name="list-create-task"
    ),

    path(
        "task-detail/<int:pk>/",
        TaskRetrieveUpdateAPIView.as_view(),
        name="retrieve-update-task"
    ),

    path(
        "task-accept/<int:pk>/",
        TaskAcceptAPIView.as_view(),
        name="accept-task"
    ),

]
