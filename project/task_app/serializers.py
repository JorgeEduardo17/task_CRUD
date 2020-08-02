from rest_framework import serializers
from .models import TaskUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUser
        fields = [
            "name",
            "user",
            "description",
            "date",
            "accept",
            "reason",
        ]
        read_only = ["id"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
