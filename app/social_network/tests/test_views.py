import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from social_network.models import Comment, Post, User


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

    @pytest.mark.django_db
    def test_see_posts_from_user_unauthorized_fail(self, api_client: APIClient):
        created_user = User.objects.create(username="usuário", password="senha")
        url = reverse("list_posts_from_user", kwargs={"username": created_user.username})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_get_post_by_id_is_sucess(self, api_client: APIClient):
        user = User.objects.create(username="Robertin", password="senha")
        post = Post.objects.create(title="Robervaldo CD's", content="O melhor do arrocha", user=user)
        url = reverse("post_details", kwargs={"pk": post.id})

        response = api_client.get(url)
        data = response.data
        assert response.status_code == status.HTTP_200_OK
        assert data["content"] == post.content
        assert data["title"] == post.title

    @pytest.mark.django_db
    def test_create_post_with_no_credenentials_fail(self, api_client: APIClient):
        url = reverse("create_list_post")
        payload = {
            "title": "teste testando testes",
            "content": "teste testa testes e fica testado",
        }
        response = api_client.post(url, payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Post.objects.count() == 0

    @pytest.mark.django_db
    def test_get_all_posts_is_sucess(self, api_client: APIClient):
        url = reverse("create_list_post")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


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
    def test_create_post_is_sucess(self, api_client: APIClient, created_user: User):
        url = reverse("create_list_post")
        payload = {
            "title": "teste testando testes",
            "content": "teste testa testes e fica testado",
        }
        response = api_client.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        post = Post.objects.get(user=created_user)
        # Assegurando que todos os itens do payload são iguais ao post criado
        for key, value in payload.items():
            assert getattr(post, key) == value

    @pytest.mark.django_db
    def test_see_posts_from_user_is_sucess(self, api_client: APIClient, created_user: User):
        payload = {
            "title": "Meu postzinho lindinho",
            "content": "O que será de mim sem testes?",
            "user": created_user,
        }
        post_created = Post.objects.create(**payload)
        Comment.objects.create(user=created_user, post=post_created, content="halysson")
        url = reverse("list_posts_from_user", kwargs={"username": created_user.username})

        response = api_client.get(url)
        posts = list(response.data)

        post_response = posts[0]

        assert response.status_code == status.HTTP_200_OK

        assert len(posts) == 1

        assert "user" in post_response

        assert "comments" in post_response

        assert post_response["title"] == post_created.title
        assert post_response["content"] == post_created.content
        assert post_response["created_at"] == post_created.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        assert post_response["updated_at"] == post_created.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        assert created_user.username == payload["user"].username

    @pytest.mark.django_db
    def test_create_post_invalid_dates_fail(self, api_client: APIClient, created_user: User):
        url = reverse("create_list_post")
        payload = {
            "title": "teste testando testes",
            "content": "teste testa testes e fica testado",
            "created_at": "1998-04-30T02:29:06.010088Z",
            "updated_at": "1998-04-30T02:29:06.010088Z",
        }
        response = api_client.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["created_at"] != payload["created_at"]
        assert response.data["created_at"] != payload["updated_at"]

    @pytest.mark.django_db
    def test_create_post_with_no_required_content_fail(self, api_client: APIClient, created_user: User):
        url = reverse("create_list_post")
        payload = {
            "title": "",
            "content": "",
        }
        response = api_client.post(url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
