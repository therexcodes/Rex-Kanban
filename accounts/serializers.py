from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True) #confirm password Field
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password" :  "Passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove confrim password field
        user = User.objects.create_user(**validated_data) # Create User
        return user