from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.contrib.auth.password_validation import validate_password

from users.models import User
from users.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(
            validate_username,
            UniqueValidator(queryset=User.objects.all()),
        )
    )

    class Meta:
        model = User
        fields = (
            'pk', 'username', 'first_name', 'last_name', 'email', 'role'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            ),
        ]


class SignupSerializer(serializers.Serializer):
    """Serilizer for authorization using e-mail."""
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username,)
    )
    password = serializers.CharField(
        required=True,
        validators=(validate_password,),
    )


class TokenSerializer(serializers.Serializer):
    """Serilizer for the token."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(required=True, max_length=150)


class LoginSerializer(serializers.Serializer):
    """Serializer for the login"""
    email = serializers.EmailField(required=True, max_length=254)
    password = serializers.CharField(
        required=True,
        validators=(validate_password,),
    )


class OtpSerializer(serializers.Serializer):
    """Serializer for verify OTP"""
    email = serializers.EmailField(required=True, max_length=254)
    otp = serializers.CharField(
        max_length=6,
        required=True,
    )
