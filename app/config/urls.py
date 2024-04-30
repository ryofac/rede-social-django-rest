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
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from social_network import views

router = routers.DefaultRouter()
urlpatterns = [
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    path("api/", include(router.urls)),
    path("api/auth/login/", views.LoginView.as_view(), name="login"),
    path("api/auth/signup/", views.SignupView.as_view(), name="signup"),
    path("api/auth/signout/", views.SignoutView.as_view(), name="signout"),
    path("api/posts", views.CreateListPost.as_view(), name="create_post"),
    path("api/posts/<str:username>", views.ListPostsFromUser.as_view(), name="list_posts_from_user"),
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
