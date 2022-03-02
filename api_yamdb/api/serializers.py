from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

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
    review = SlugRelatedField(slug_field='text', many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
