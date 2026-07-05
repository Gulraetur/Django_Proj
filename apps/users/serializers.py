from rest_framework import serializers
from .models import User, ClientProfile, ExecutorProfile

class UserSerializer(serializers.ModelSerializer):
    client_profile = serializers.PrimaryKeyRelatedField(read_only=True)
    executor_profile = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'avatar', 'client_profile', 'executor_profile')
        read_only_fields = ('id',)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone', 'avatar')
        extra_kwargs = {
            'phone': {'required': False},
            'avatar': {'required': False},
        }
    def create(self, validated_data):
        role = self.initial_data.get('role', 'customer')
        user = User.objects.create_user(**validated_data)
        if role == 'executor':
            ExecutorProfile.objects.create(user=user)
        else:
            ClientProfile.objects.create(user=user)
        return user