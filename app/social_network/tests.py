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
    def test_signup_passwords_does_not_match_fail(self, api_client: APIClient):
        url = reverse("signup")
        payload = {
            "username": "tcheu amigo",
            "email": "teuamigo@gmail.com",
            "password": "tcha_prima123$",
            "confirm_password": "123",
            "first_name": "tcheu",
            "last_name": "amigo",
        }
        response = api_client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_signup_without_required_field_fail(self, api_client: APIClient):
        url = reverse("signup")
        payload = {
            "username": "tcheu amigo",
            "password": "tcha_prima123$",
            "confirm_password": "123",
            "first_name": "tcheu",
            "last_name": "amigo",
        }
        response = api_client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_login_with_wrong_credentials_fail(self, api_client: APIClient):
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
            "username": user_created.email + "123",
            "password": user_created.email + "123",
        }
        response = api_client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_login_with_username_instead_of_email_fail(self, api_client: APIClient):
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
            "username": user_created.username,
            "password": kwargs["password"],
        }
        response = api_client.post(url, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_sign_out_not_logged_in_fail(self, api_client: APIClient):
        url = reverse("signout")
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


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

    @pytest.mark.django_db
    def test_log_in_already_logged_in_fail(self, api_client: APIClient, created_user: User):
        pass
