from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.authtoken.models import Token
from .models import User

factory = APIRequestFactory

class SocialNetworkTestCase(APITestCase):
    def test_signup(self):
        url = reverse("signup")
        userfake = {"username":"tcheu amigo",
                    "email": "teuamigo@gmail.com",
                    "first_name":"tcheu",
                    "last_name":"amigo"}
        response = self.client.post(url, userfake, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

        user_created = User.objects.get(username=userfake["username"])
        token_created = response.data["token"]

        tokenDb = Token.objects.get(key=token_created)
        self.assertEqual(tokenDb.user, user_created)

    def test_logout(self):
        pass

    def test_test_token(self):
        pass

    