from rest_framework import serializers
from .models import Task, TaskMaterial
from apps.users.serializers import UserSerializer
from django.utils.text import slugify

class TaskSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    executor = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'client', 'executor', 'created_at', 'updated_at', 'slug')  # slug read-only

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data.get('title', ''))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data['title']
        instance.slug = slugify(instance.title)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class TaskMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskMaterial
        fields = ('id', 'task', 'title', 'result_file', 'url', 'created_at')
        read_only_fields = ('id', 'task', 'created_at')

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Название не может быть пустым")
        return value

    def validate(self, data):
        if not data.get('result_file') and not data.get('url'):
            raise serializers.ValidationError("Необходимо указать файл или ссылку")
        return data