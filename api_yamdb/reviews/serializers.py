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

