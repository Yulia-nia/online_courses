from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()  # empty values
    time_update = serializers.DateTimeField(read_only=True) # автоматически
    # Чтобы сериализатор корректно обрабатывал эти поля, в их определении нужно добавить аргумент read_only=True:
    time_create = serializers.DateTimeField(read_only=True)
    # category_id = serializers.IntegerField()

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.save()
        return instance

    # class Meta:
    #     model = Course
    #     fields = ('title', 'description', 'time_update')
