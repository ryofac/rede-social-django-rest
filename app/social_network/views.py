from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from social_network.models import Post, PostInteraction, User
from social_network.serializers import (
    CommentSerializer,
    PostInteractionSerializer,
    PostSerializer,
    UserLoginSerializer,
    UserSerializer,
)


# Login and Register Views:
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        # Validando a entrada:
        serializer = UserLoginSerializer(data=data, context={"request": request})
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = serializer.validated_data["user"]
            # Obtendo ou criando um token para esse usuário
            token, created = Token.objects.get_or_create(user=user)  # retorna (token, bool)
            # atualizando manualmente o last_login
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
            return Response({"token": token.key})

        except User.DoesNotExist:
            return Response({"detail": "The required user does not exist"}, status=status.HTTP_404_NOT_FOUND)


class SignupView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data, context={"request": request})

        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Salvando o usuário a ser criado:
        serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)


class SignoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        logged_user = request.user
        logged_user.auth_token.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CreatePost(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer

    def post(self, request):
        user = request.user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListPostsFromUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer

    def get(self, request, username: str):
        posts = Post.objects.filter(user__username=username)
        serializer = PostSerializer(posts, many=True)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class PostDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(request):
        pass

    def post(request):
        pass

    def patch(request):
        pass

    def delete(request):
        pass


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    # TODO: Implementar usuário autenticado
    user = request.user
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=404)

    try:
        # Verificando se usuário já curtiu o post:
        like = PostInteraction.objects.get(user=user, post=post, interaction_type=PostInteraction.LIKE)
        like.delete()  # Remove a curtida
        return Response({"message": "Post descurtido com sucesso"})
    except PostInteraction.DoesNotExist:
        # Remove qualquer descurtida que o usuário tenha dado anteriormente
        PostInteraction.objects.filter(user=user, post=post, interaction_type=PostInteraction.DISLIKE).delete()
        # Adiciona a curtida
        PostInteraction.objects.create(user=user, post=post, interaction_type=PostInteraction.LIKE)
        return Response({"message": "Post curtido com sucesso"})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def toggle_dislike(request, post_id):
    # TODO: Implementar usuário autenticado
    user = request.user
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=404)

    try:
        # Verificando se usuário já curtiu o post:
        dislike = PostInteraction.objects.get(user=user, post=post, interaction_type=PostInteraction.DISLIKE)
        dislike.delete()  # Remove a descurtida
        return Response({"message": "Descurtida removida com sucesso"})
    except PostInteraction.DoesNotExist:
        # Remove qualquer curtida que o usuário tenha dado no post anteriormente
        PostInteraction.objects.filter(user=user, post=post, interaction_type=PostInteraction.LIKE).delete()
        # Adiciona a descurtida
        PostInteraction.objects.create(user=user, post=post, interaction_type=PostInteraction.DISLIKE)
        return Response({"message": "Post descurtido com sucesso"})


# USER:


# TODO: Implementar list_all_friends_from_user passando o id do usuário desejado
@api_view(["GET"])
def list_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# alterar os metodos, acho que nao estao funcionando :)
@api_view(["GET"])
def list_followed_by(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    followed_by = user.followed_by.all()
    serializer = UserSerializer(followed_by, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def list_followers(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    followers = user.followers.all()
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def list_comments_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=404)

    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=404)

    user = request.user
    post_interaction = PostInteraction.objects.create(user=user, post=post, interaction_type=PostInteraction.LIKE)
    serializer = PostInteractionSerializer(post_interaction)
    return Response(serializer.data, status=201)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deslike_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=404)

    user = request.user
    post_interaction = PostInteraction.objects.create(user=user, post=post, interaction_type=PostInteraction.DISLIKE)
    serializer = PostInteractionSerializer(post_interaction)
    return Response(serializer.data, status=201)


"""
test_token: endpoint que serve somente para indicar se o token de autenticação de usuário está funcionando
"""


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    serializer = UserSerializer(request.user)
    token = Token.objects.get(user=request.user)
    return Response({"detail": "Authenticated", "token": token.key, "user": serializer.data})
