from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    time_update = serializers.DateTimeField(read_only=True)
    time_create = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.save()
        return instance

