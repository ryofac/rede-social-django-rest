"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework import routers
from social_network import views

router = routers.DefaultRouter()
# TODO: primeiro implementar as rotas de authenticacao testadas para depois continuar implementando o resto
urlpatterns = [
    path("", include(router.urls)),
    path("api/auth/login/", views.login),
    path("user/<str:username>/logout/)", views.logout),
    path("signup/", views.signup, name="signup"),
]
#     path("test/token/", views.test_token),
#     path("posts/", views.create_list_post),
#     path("users/", views.list_all_users),
#     # gets by username and post
#     # se quiserem alterar o nome, a vontade
#     path("users/<str:username>/followed_by/", views.list_followed_by),
#     path("users/<str:username>/followers/", views.list_followers),
#     path("post/<int:pk>/comments/", views.list_comments_post),
#     # levando junto o usuário autenticado
#     path("post/<int:pk>/like/", views.like_post),
#     path("post/<int:pk>/deslike/", views.deslike_post),
