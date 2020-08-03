from rest_framework import serializers
from .models import TaskUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUser
        fields = [
            "id",
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


class AcceptTaskSerializer(serializers.ModelSerializer):
    reason = serializers.CharField(required=True)
    accept = serializers.BooleanField(required=True)

    class Meta:
        model = TaskUser
        fields = [
            "id",
            "accept",
            "reason",
        ]
        read_only = ["id"]

    def update(self, instance, validated_data):
        reason = validated_data.pop("reason")
        accept = validated_data.pop("accept")
        instance.reason = reason
        instance.accept = accept
        instance.save()
        return instance
