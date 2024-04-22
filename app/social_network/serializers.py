from rest_framework import serializers
from social_network import models


# TODO: Pesquisar sobre ordenamento das classes
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "password",
            "followers",
            "full_name",
            "first_name",
            "last_name",
            "last_login",
            "is_authenticated",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"write_only": True},
            "last_name": {"write_only": True},
        }
        read_only_fields = ["id", "full_name", "last_login"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = models.Comment
        fields = ["id", "content", "user"]
        read_only_fields = ["id", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = models.Post
        fields = ["id", "title", "content", "created_at", "updated_at", "comments", "user"]
        read_only_fields = ["id", "created_at"]
