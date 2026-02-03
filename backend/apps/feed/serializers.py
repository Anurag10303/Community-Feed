from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "children",
        )

    def get_children(self, obj):
        """
        Recursive serialization.
        Assumes `.children` is already populated by selector.
        """
        if not hasattr(obj, "children"):
            return []

        return CommentSerializer(obj.children, many=True).data

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "comments",
        )
