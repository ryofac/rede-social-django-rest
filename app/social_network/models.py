from django.contrib.auth.models import AbstractUser
from django.db import models


# TODO: Analisar Abstract User e adaptar esse model
class User(AbstractUser):
    username = models.CharField(max_length=20, verbose_name="Nome de usuário", unique=True)
    name = models.CharField(max_length=45, verbose_name="Nome")
    password = models.CharField(verbose_name="Senha")
    bio = models.CharField(max_length=255, verbose_name="Biografia")
    followers = models.ManyToManyField("self", symmetrical=False, related_name="Followed", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]


class Post(models.Model):
    title = models.TextField(blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=255, verbose_name="Conteúdo")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class PostInteraction(models.Model):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"

    INTERACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
