"""
Arquivo que contém todas as fixtures utilizadas nos testes do pytest
"""

import pytest
from rest_framework.test import APIClient
from social_network.models import Post, User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def api_client_authenticated(created_user: User):
    user = created_user
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def created_user(**kwargs):
    user_data = {
        "username": "tcheu amigo",
        "email": "teuamigo@gmail.com",
        "password": "tcha_prima123$",
        "first_name": "tcheu",
        "last_name": "amigo",
    }
    user_data.update(kwargs)
    user_created = User.objects.create_user(**user_data)
    return user_created


@pytest.fixture
def created_post(created_user: User, **kwargs):
    post_data = {
        "title": "titulo padrao",
        "content": "conteudo padrao",
        "user": created_user,
    }

    post_data.update(kwargs)
    created_post = Post.objects.create(**post_data)
    return created_post
