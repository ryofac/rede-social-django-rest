from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from social_network.models import Post, PostInteraction, User
from social_network.serializers import CommentSerializer, PostInteractionSerializer, PostSerializer, UserSerializer


class CreateListPost(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer

    # ?: Sobrescrita de métodos devido as diverenças de permissões entre a listagem e a criação
    def get_authenticators(self):
        if not self.request:
            super().get_authenticators()
        if self.request.method == "POST":
            return [SessionAuthentication()]  # Autenticador para requisições POST
        elif self.request.method == "GET":
            return [BasicAuthentication()]  # Autenticador para requisições GET
        return super().get_authenticators()

    def get_permissions(self):
        if not self.request:
            return super().get_permissions()
        if self.request and self.request.method == "POST":
            return [IsAuthenticated()]  # Permissão para requisições POST
        elif self.request and self.request.method == "GET":
            return [AllowAny()]  # Permissão para requisições GET
        return super().get_permissions()

    def get(self, request):
        self.authentication_classes = []
        self.permission_classes = [AllowAny]
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
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
