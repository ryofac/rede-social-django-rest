import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from social_network.models import Comment, Post, User


# Testes com o usuário não logado
class TestPublicSocialNetworkViews:
    @pytest.mark.django_db
    def test_signup_is_success(self, api_client: APIClient):
        url = reverse("social_network:signup")
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
        url = reverse("social_network:login")

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
        url = reverse("social_network:signup")
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
        url = reverse("social_network:signup")
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
        url = reverse("social_network:login")
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
        url = reverse("social_network:login")
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
        url = reverse("social_network:signout")
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_see_posts_from_user_unauthorized_fail(self, api_client: APIClient):
        created_user = User.objects.create(username="usuário", password="senha")
        url = reverse("social_network:list_posts_from_user", kwargs={"username": created_user.username})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_get_post_by_id_is_sucess(self, api_client: APIClient):
        user = User.objects.create(username="Robertin", password="senha")
        post = Post.objects.create(title="Robervaldo CD's", content="O melhor do arrocha", user=user)
        url = reverse("social_network:post_details", kwargs={"pk": post.id})

        response = api_client.get(url)
        data = response.data
        assert response.status_code == status.HTTP_200_OK
        assert data["content"] == post.content
        assert data["title"] == post.title

    @pytest.mark.django_db
    def test_create_post_with_no_credenentials_fail(self, api_client: APIClient):
        url = reverse("social_network:create_list_post")
        payload = {
            "title": "teste testando testes",
            "content": "teste testa testes e fica testado",
        }
        response = api_client.post(url, payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Post.objects.count() == 0

    @pytest.mark.django_db
    def test_get_all_posts_is_sucess(self, api_client: APIClient):
        url = reverse("social_network:create_list_post")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_acessing_me_not_authenticated_failing(self, api_client: APIClient):
        url = reverse("social_network:user-me")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_get_all_users_is_sucess(self, api_client: APIClient):
        url = reverse("social_network:user-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == User.objects.count()

    def test_update_user_unauthenticated_fail(self, api_client):
        url = reverse("social_network:user-update")
        response = api_client.patch(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Testes com o usuário logado
class TestPrivateSocialNetworkViews:
    @pytest.mark.django_db
    def test_signout_is_success(self, api_client_authenticated: APIClient, created_user: User):
        Token.objects.create(user=created_user)
        url = reverse("social_network:signout")
        response = api_client_authenticated.post(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Token.objects.filter(user=created_user).exists() is False

    @pytest.mark.django_db
    def test_create_post_is_sucess(self, api_client_authenticated: APIClient, created_user: User):
        url = reverse("social_network:create_list_post")
        payload = {
            "title": "teste testando testes",
            "content": "teste testa testes e fica testado",
        }
        response = api_client_authenticated.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        post = Post.objects.get(user=created_user)
        # Assegurando que todos os itens do payload são iguais ao post criado
        for key, value in payload.items():
            assert getattr(post, key) == value

    @pytest.mark.django_db
    def test_see_posts_from_user_is_sucess(self, api_client_authenticated: APIClient, created_user: User):
        payload = {
            "title": "Meu postzinho lindinho",
            "content": "O que será de mim sem testes?",
            "user": created_user,
        }
        post_created = Post.objects.create(**payload)
        Comment.objects.create(user=created_user, post=post_created, content="halysson")
        url = reverse("social_network:list_posts_from_user", kwargs={"username": created_user.username})

        response = api_client_authenticated.get(url)
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
    def test_create_post_invalid_dates_fail(self, api_client_authenticated: APIClient, created_user: User):
        url = reverse("social_network:create_list_post")
        payload = {
            "title": "teste testando testes",
            "content": "teste testa testes e fica testado",
            "created_at": "1998-04-30T02:29:06.010088Z",
            "updated_at": "1998-04-30T02:29:06.010088Z",
        }
        response = api_client_authenticated.post(url, payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["created_at"] != payload["created_at"]
        assert response.data["created_at"] != payload["updated_at"]

    @pytest.mark.django_db
    def test_create_post_with_no_required_content_fail(self, api_client_authenticated: APIClient, created_user: User):
        url = reverse("social_network:create_list_post")
        payload = {
            "title": "",
            "content": "",
        }
        response = api_client_authenticated.post(url, payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_update_post_is_sucess(self, api_client_authenticated: APIClient, created_post: Post):
        url = reverse("social_network:post_details", kwargs={"pk": created_post.id})
        payload = {"title": "Titulo atualizado", "content": "Conteudo atualizado"}
        response = api_client_authenticated.patch(url, payload)

        assert response.status_code == status.HTTP_200_OK
        assert Post.objects.count() == 1

        # Assegurando que todos os itens do payload são iguais ao post alterado
        altered_post = Post.objects.get(id=created_post.id)
        for key, value in payload.items():
            assert getattr(altered_post, key) == value

    @pytest.mark.django_db
    def test_delete_post_is_sucess(self, api_client_authenticated: APIClient, created_post: Post):
        url = reverse("social_network:post_details", kwargs={"pk": created_post.id})
        response = api_client_authenticated.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Post.objects.count() == 0

    @pytest.mark.django_db
    def test_delete_post_dosent_exists_fail(self, api_client_authenticated: APIClient, created_post: Post):
        created_post_id = created_post.id
        created_post.delete()
        url = reverse("social_network:post_details", kwargs={"pk": created_post_id})
        response = api_client_authenticated.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_post_dosent_exists_fail(self, api_client_authenticated: APIClient, created_post: Post):
        created_post_id = created_post.id
        created_post.delete()
        url = reverse("social_network:post_details", kwargs={"pk": created_post_id})
        payload = {"title": "Titulo atualizado", "content": "Conteudo atualizado"}
        response = api_client_authenticated.patch(url, payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_post_from_other_user_fail(self, api_client_authenticated: APIClient):
        other_user = User.objects.create(username="other-user", password="123321")
        post_from_other_user = Post.objects.create(title="a", content="b", user=other_user)
        url = reverse("social_network:post_details", kwargs={"pk": post_from_other_user.id})
        payload = {"title": "Titulo atualizado", "content": "Conteudo atualizado"}
        response = api_client_authenticated.patch(url, payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_delete_post_from_other_user_fail(self, api_client_authenticated: APIClient):
        other_user = User.objects.create(username="other-user", password="123321")
        post_from_other_user = Post.objects.create(title="a", content="b", user=other_user)
        url = reverse("social_network:post_details", kwargs={"pk": post_from_other_user.id})
        response = api_client_authenticated.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_if_me_is_working(self, api_client_authenticated: APIClient, created_user):
        url = reverse("social_network:user-me")
        response = api_client_authenticated.get(url)

        assert response.status_code == status.HTTP_200_OK

        user_data = response.data
        for key in ["username", "email", "last_login"]:
            assert key in user_data.keys()

        assert user_data["username"] == created_user.username
        assert user_data["email"] == created_user.email

    @pytest.mark.django_db
    def test_me_acessing_from_unlogged_user(self, api_client_authenticated: APIClient, created_user):
        api_client_authenticated.logout()
        url = reverse("social_network:user-me")
        response = api_client_authenticated.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
