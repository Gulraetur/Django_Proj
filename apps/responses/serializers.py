from rest_framework import serializers
from .models import Response
from apps.users.serializers import UserSerializer
from apps.tasks.serializers import TaskSerializer

class ResponseSerializer(serializers.ModelSerializer):
    executor = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Response
        fields = '__all__'
        read_only_fields = ('id', 'executor', 'created_at', 'status')