from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from social_network import models

from django.contrib.auth.models import Group, User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "username", "password", "followers"]
        extra_kwargs = {"password" : {"write_only" : True}}

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = models.Comment
        fields = "__all__"
        read_only_fields = ["created_at"]

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = models.Post
        fields = ["id", "title", "content", "created_at", "updated_at", "comments", "user"]
        read_only_fields = ["created_at"]
