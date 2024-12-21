from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Automatically set the current user

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user']  # Ensures that 'user' is not included in the input request, only in the response.


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)