from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from social_network.models import Post, PostInteraction, User
from social_network.serializers import CommentSerializer, PostSerializer, UserSerializer, PostInteractionSerializer



# Login and Register Views:
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def login(request):
    data = request.data
    # Validando a entrada: Username e Password
    # TODO: Pode ser que seja melhor ter um Serializer aqui
    if not data.get("username") or not data.get("password"):
        return Response(data={"detail": "invalid username or password"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        # Obtendo um usuário com o método authenticate
        user = authenticate(request, username=data["username"], password=data["password"])

        # Checando se existe o usuário e a senha usando o check_password (já verifica o hash)
        if not user or not user.check_password(request.data["password"]):
            return Response({"detail": "The required user does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Obtendo ou criando um token para esse usuário
        token, created = Token.objects.get_or_create(user=user)  # retorna (token, bool)
        serializer = UserSerializer(user)

        # atualizando manualmente o last_login
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        return Response({"token": token.key, "user": serializer.data})

    except User.DoesNotExist:
        return Response({"detail": "The required user does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def signup(request):
    data = request.data

    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        # Salvando o usuário a ser criado:
        serializer.save()

        # Buscando o usuário:
        created_user = User.objects.get(username=data["username"])

        # Hasheando a senha:
        created_user.set_password(data["password"])
        created_user.save()

        # Criando um token de autenticação para esse usuário:
        token = Token.objects.create(user=created_user)

        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    if not request.user or not request.user.is_authenticated:
        print(request.user.__dict__)
        return Response({"detail": "not logged in"}, status=status.HTTP_400_BAD_REQUEST)
    logged_user = request.user
    logged_user.auth_token.delete()
    django_logout(request)
    return Response({"detail": "sucessfuly logged out"}, status=status.HTTP_200_OK)


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


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_list_post(request, format=None):
    user = request.user
    match request.method:
        case "GET":
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        case "POST":
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                # user = request.user
                serializer.save(user=user)
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(data={"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        case _:
            return Response(data=None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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

#alterar os metodos, acho que nao estao funcionando :)
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