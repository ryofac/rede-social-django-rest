from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=20, verbose_name="Nome de usuário", unique=True)
    email = models.EmailField(verbose_name="Email do Usuário", unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Nome")
    last_name = models.CharField(max_length=30, verbose_name="Sobrenome")
    password = models.CharField(verbose_name="Senha")
    bio = models.CharField(max_length=255, verbose_name="Biografia")
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="followed", blank=True, verbose_name="Seguidores"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]


class Post(models.Model):
    title = models.TextField(blank=False, verbose_name="Título")
    content = models.TextField(blank=False, verbose_name="Conteúdo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Alterado em")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")


class Comment(models.Model):
    content = models.CharField(max_length=255, verbose_name="Conteúdo")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Postagem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")


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
