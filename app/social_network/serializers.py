from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from social_network import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "followers",
            "full_name",
            "first_name",
            "last_name",
            "last_login",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

        read_only_fields = ["id", "full_name", "last_login", "followers"]

    def validate(self, attrs):
        validate_password(attrs["password"])
        return super().validate(attrs)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if not email or not password:
            raise serializers.ValidationError("Email or password not provided", code="authorization")
        try:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials", code="authorization")
            attrs["user"] = user
            return attrs

        except exceptions.ValidationError:
            raise serializers.ValidationError("Invalid password", code="authorization")


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


class PostInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostInteraction
        fields = ["id", "post", "user", "like", "deslike"]
        read_only_fields = ["id"]
