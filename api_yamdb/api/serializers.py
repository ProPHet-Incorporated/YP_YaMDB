from datetime import datetime

from rest_framework import serializers

from reviews.models import Categories, Genre, Title


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class DefaultTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, data):
        if data.get('year') and data['year'] > datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска произведения не может быть в будущем'
            )
        return data


class PostTitleSerializer(DefaultTitleSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field='slug'
    )


class GetTitleSerializer(DefaultTitleSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
