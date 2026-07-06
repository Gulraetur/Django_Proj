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
        read_only_fields = ('id', 'client', 'executor', 'created_at', 'updated_at')

    def generate_unique_slug(self, title, instance=None):
        """Генерирует уникальный slug на основе title."""
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Task.objects.filter(slug=slug).exclude(pk=instance.pk if instance else None).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def create(self, validated_data):
        if not validated_data.get('slug'):
            validated_data['slug'] = self.generate_unique_slug(validated_data.get('title', ''))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        title_changed = 'title' in validated_data and validated_data['title'] != instance.title
        slug_provided = 'slug' in validated_data
        slug_value = validated_data.get('slug')

        if title_changed:
            if not slug_provided or not slug_value or slug_value == instance.slug:
                validated_data['slug'] = self.generate_unique_slug(validated_data['title'], instance)
        else:
            if slug_provided and not slug_value:
                validated_data['slug'] = self.generate_unique_slug(instance.title, instance)

        return super().update(instance, validated_data)
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