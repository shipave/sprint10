import datetime
import re

from rest_framework import serializers

from users.models import User
from reviews.models import Category, Genre, Title, Comment, Review


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(
        source='reviews__score__avg',
        read_only=True
    )
    year = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('__all__')


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True,   
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True,
    )
    year = serializers.IntegerField()

    class Meta:
        model = Title
        # fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
        fields = ('__all__')

    def validate_year(self, obj):
        """Проверка что год выпуска произведения не больше текушего."""
        if datetime.datetime.now().year < obj:
            raise serializers.ValidationError("The title from future?")
        return obj


class ReviewSerializer(serializers.ModelSerializer):
    comment = serializers.SlugRelatedField(
        read_only=False, slug_field='slug',
        queryset=Comment.objects.all(),
        required=False)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date', 'comment')
        


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text')


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
