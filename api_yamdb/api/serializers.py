from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title
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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

from reviews.models import Comment, Review  # isort:skip


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='id', many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = SlugRelatedField(slug_field='text', many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


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


class TokenSerializer(TokenObtainPairSerializer):

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'token': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CustomUser
