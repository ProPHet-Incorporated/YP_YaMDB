from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError

from users.validators import validate_username

User = get_user_model()


class CustomUsernameField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get(
            'max_length',
            settings.USERNAME_LENGTH
        )
        self.validators.append(validate_username)
        super().__init__(*args, **kwargs)


class UserSerializer(serializers.ModelSerializer):
    username = CustomUsernameField(
        required=True,
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_LENGTH,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MeSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    username = CustomUsernameField(
        required=True,
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_LENGTH,
        required=True,
    )

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']
        if not User.objects.filter(username=username, email=email).exists():
            if User.objects.filter(email=email).exists():
                raise ValidationError(f'{username} - уже занят.')
            if User.objects.filter(username=username).exists():
                raise ValidationError(f'{email} - уже занят.')
        return attrs


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
