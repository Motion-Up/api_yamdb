from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Comment, Review
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        # fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = '__all__'
        exclude = ('id',)
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(source='reviews__score__avg', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(slug_field='id', many=False, read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                'Выуже оставили отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    review = serializers.SlugRelatedField(slug_field='text', many=False, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):

    queryset = CustomUser.objects.all()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=queryset)],
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class RegisterSerializer(serializers.ModelSerializer):

    queryset = CustomUser.objects.all()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=queryset)],
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = CustomUser
        lookup_field = 'username'


class OwnerSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = CustomUser
        lookup_field = 'username'


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
