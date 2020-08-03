from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_app.pagination import TasPagination
from task_app.permission import IsUserOwnerTAskAuthenticated
from .models import TaskUser
from .serializers import TaskSerializer


class TaskAPIView(generics.ListCreateAPIView):
    name = "list-create-task"
    queryset = TaskUser.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    pagination_class = TasPagination

    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    name = "retrieve-update-task"
    queryset = TaskUser.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsUserOwnerTAskAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, obj=instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
