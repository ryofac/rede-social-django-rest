from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from social_network.models import Post, PostInteraction, User
from social_network.serializers import PostSerializer


# Login and Register Views:
@api_view(["POST"])
def login(request):
    pass


@api_view(["POST"])
def signup(request):
    pass


@api_view(["GET"])
def test_token(request):
    pass


@api_view(["GET", "POST"])
def create_list_post(request, format=None):
    match request.method:
        case "GET":
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        case "POST":
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                post_saved = serializer.save()
                return Response(post_saved, status=status.HTTP_201_CREATED)
            return Response(data={"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        case _:
            return Response(data=None, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
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


@api_view(["POST, GET"])
def create_list_user(request):
    match request.method:
        case "POST":
            data = request.data
            User.objects.create(
                username=data["username"],
                name=data["name"],
            )
