from django.urls import path
from social_network import views

app_name = "social_network"


urlpatterns = [
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/signup/", views.SignupView.as_view(), name="signup"),
    path("auth/signout/", views.SignoutView.as_view(), name="signout"),
    path("posts/", views.CreateListPost.as_view(), name="create_list_post"),
    path("posts/<int:pk>/", views.PostDetails.as_view(), name="post_details"),
    path("user/<str:username>/posts/", views.ListPostsFromUser.as_view(), name="list_posts_from_user"),
]
