from django.urls import path

from .views import TaskAPIView, TaskRetrieveUpdateAPIView

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

]
