from rest_framework import serializers
from reviews.models import User

import api.views


class SignUpSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if "me" == value.lower():
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        return value

    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        obj = User.objects.create_user(**validated_data)
        # вызов функции отправки сообщения на почту
        api.views.send_message(
            validated_data['email'],
            validated_data['username']
        )
        return obj


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        model = User
        read_only_fields = ('role',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
