from rest_framework import serializers
from reviews.models import User, UserAuth
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.relations import SlugRelatedField
import api.views


class SignUpSerializer(serializers.ModelSerializer):
    #username = serializers.CharField()

    def validate_username(self, value):
        if "me" == value.lower():
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        return value

    class Meta:
        model = User
        fields = ['email', 'username']

    def create(self, validated_data):
        obj = User.objects.create_user(**validated_data)
        # вызов функции отправки сообщения на почту
        api.views.send_message(
            validated_data['email'],
            validated_data['username']
        )
        return obj


"""class GetTokenSerializer(TokenObtainSerializer):
    print('GHDHKAJSGDAHJGDSAJ')
    user = SlugRelatedField(
        slug_field='username',
        queryset=UserAuth.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    #password = serializers.ReadOnlyField()

    def validate_password(self, value):
        print('EOT PASDASD', value['password'])
        if len(value['password']) == 0:
            value = 'asdsadasd'
            return value

    class Meta:
        fields = ['user', 'confirmation_code']
        read_only = "password"
"""

"""class MyTokenObtainSerializer(GetTokenSerializer):
    
    class Meta:
        fields = ['user', 'confirmation_code']
        read_only = "password"""


class GetTokenSerializer(serializers.ModelSerializer):
    print('ZDES BILI------------------------------------------------------------------')
    """username = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )"""
    
    confirm_code = serializers.ReadOnlyField()

    def validate(self, data):
        if data['confirmation_code'] != UserAuth.objects.get(username=data['username']).confirmation_code:
            raise serializers.ValidationError(
                "Неверный код подтверждения!"
            )
        return data

    class Meta:
        model = UserAuth
        fields =  ['username', 'confirmation_code', 'confirm_code']

