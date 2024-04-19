from django.db import models
from django.db.models.functions import Now


class User(models.Model):
    username = models.CharField(max_length=20, verbose_name="Nome de usuário")
    password = models.CharField(max_length=20, verbose_name="Senha")
    followers = models.ManyToManyField('self', symmetrical=False, related_name="Followed", blank=True)

class Post(models.Model):
    title = models.TextField(blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_created=True, default= Now())
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.CharField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)