from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task_app.pagination import TasPagination
from task_app.permission import IsUserOwnerTAskAuthenticated
from .models import TaskUser
from .serializers import TaskSerializer, AcceptTaskSerializer


class TaskAPIView(generics.ListCreateAPIView):
    name = "list-create-task"
    queryset = TaskUser.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    pagination_class = TasPagination

    def get_queryset(self):
        queryset = self.queryset

        filters = {}

        if self.request.GET.get("search"):
            filters.update(description__icontains=self.request.GET.get("search"))

        queryset = queryset.filter(**filters)

        return queryset

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


class TaskAcceptAPIView(generics.UpdateAPIView):
    name = "accept-task"
    queryset = TaskUser.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsUserOwnerTAskAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, obj=instance)
        serializer = AcceptTaskSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data)
