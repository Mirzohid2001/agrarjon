from rest_framework import serializers

from .models import User, Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname','password', 'email', 'phone', 'created_at', 'updated_at']