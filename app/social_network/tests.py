import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import User


# Testes com o usuário não logado
class TestPublicSocialNetworkViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.mark.django_db
    def test_signup_is_success(self, api_client: APIClient):
        url = reverse("signup")
        payload = {
            "username": "tcheu amigo",
            "email": "teuamigo@gmail.com",
            "password": "tcha_prima123$",
            "confirm_password": "tcha_prima123$",
            "first_name": "tcheu",
            "last_name": "amigo",
        }
        response = api_client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert "password" not in response.data
        user_created = User.objects.get(email=payload["email"])
        assert user_created.check_password(payload["password"])

    @pytest.mark.django_db
    def test_login_is_success(self, api_client: APIClient):
        url = reverse("login")

        kwargs = {
            "username": "tcheu amigo",
            "email": "teuamigo@gmail.com",
            "password": "tcha_prima123$",
            "first_name": "tcheu",
            "last_name": "amigo",
        }

        user_created = User.objects.create_user(**kwargs)

        payload = {
            "email": user_created.email,
            "password": kwargs["password"],
        }

        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data
        assert "password" not in response.data
        assert Token.objects.filter(user=user_created).exists() is True

    @pytest.mark.django_db
    # TODO: Implementar isso
    @pytest.mark.skip
    def test_signup_not_success(self, api_client: APIClient):
        url = reverse("signup")
        payload = {
            "username": "tcheu amigo",
            "email": "teuamigo@gmail.com",
            "password": "tcha_prima123$",
            "confirm_password": "tcha_prima123$",
            "first_name": "tcheu",
            "last_name": "amigo",
        }
        response = api_client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert "password" not in response.data
        user_created = User.objects.get(email=payload["email"])
        assert user_created.check_password(payload["password"])


# Testes com o usuário logado
class TestPrivateSocialNetworkViews:
    @pytest.fixture
    def api_client(self, created_user: User):
        user = created_user
        client = APIClient()
        client.force_authenticate(user)
        return client

    @pytest.fixture
    def created_user(self, **kwargs):
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

    @pytest.mark.django_db
    def test_signout_is_success(self, api_client: APIClient, created_user: User):
        Token.objects.create(user=created_user)
        url = reverse("signout")
        response = api_client.post(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Token.objects.filter(user=created_user).exists() is False

    def test_test_token(self):
        pass
