from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator, EmailValidator
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]*$',
                message="Username can only contain letters, numbers, and underscores.",
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            EmailValidator(
                message="Enter correct email",
            )
        ]
    )
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user