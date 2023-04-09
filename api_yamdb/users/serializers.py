import re

from rest_framework import serializers

from .models import User


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate_username(self, value):
        if not re.fullmatch(r'[\w\@\.\+\-]+', value):

            raise serializers.ValidationError('Letters, digits and @/./+/-/_ \
                                              only')
        if value == 'me':
            raise serializers.ValidationError('\'me\' not allowed')
        return value

    def validate(self, data):
        if_username = User.objects.filter(username=data['username'])
        if_email = User.objects.filter(email=data['email'])
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if if_email:
            raise serializers.ValidationError(f'adress {data["email"]} '
                                              f'is already in use')
        if if_username:
            raise serializers.ValidationError(f'Name {data["username"]} '
                                              f'is already in use')

        if data['username'] == 'me':
            raise serializers.ValidationError('\'me\' not allowed')
        return data


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'first_name',
            'last_name', 'email', 'role', 'bio'
        )
