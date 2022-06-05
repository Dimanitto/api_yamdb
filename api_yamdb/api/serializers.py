from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from reviews.models import Comment, Review, Title, User

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


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы можете добавлять только'
                                      'один отзыв на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'
