from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like


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
        if not hasattr(obj, "children"):
            return []
        return CommentSerializer(obj.children, many=True).data


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "like_count",
            "is_liked_by_user",
            "comments",
        )

    def get_is_liked_by_user(self, obj):
        request = self.context.get("request")
        if not request:
            return False

        user_id = request.query_params.get("user_id")
        if not user_id:
            return False

        return obj.likes.filter(user_id=user_id).exists()

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    children = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "like_count",
            "children",
        )
