from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from social_network.models import Post
from social_network.serializers import PostSerializer, UpdatePostSerializer

# TODO: Implementar o resto da lógica de posts:
# ! Criação/Deleção de comentários


class CreateListPost(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = PostSerializer

    def get(self, request):
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
        return Response(serializer.data)


class PostDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            post = Post.objects.get(user=request.user, id=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdatePostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk, user=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


# @api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def toggle_like(request, post_id):
#     # TODO: Implementar usuário autenticado
#     user = request.user
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return Response({"message": "Post not found"}, status=404)

#     try:
#         # Verificando se usuário já curtiu o post:
#         like = PostInteraction.objects.get(user=user, post=post, interaction_type=PostInteraction.LIKE)
#         like.delete()  # Remove a curtida
#         return Response({"message": "Post descurtido com sucesso"})
#     except PostInteraction.DoesNotExist:
#         # Remove qualquer descurtida que o usuário tenha dado anteriormente
#         PostInteraction.objects.filter(user=user, post=post, interaction_type=PostInteraction.DISLIKE).delete()
#         # Adiciona a curtida
#         PostInteraction.objects.create(user=user, post=post, interaction_type=PostInteraction.LIKE)
#         return Response({"message": "Post curtido com sucesso"})


# @api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def toggle_dislike(request, post_id):
#     # TODO: Implementar usuário autenticado
#     user = request.user
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return Response({"message": "Post not found"}, status=404)

#     try:
#         # Verificando se usuário já curtiu o post:
#         dislike = PostInteraction.objects.get(user=user, post=post, interaction_type=PostInteraction.DISLIKE)
#         dislike.delete()  # Remove a descurtida
#         return Response({"message": "Descurtida removida com sucesso"})
#     except PostInteraction.DoesNotExist:
#         # Remove qualquer curtida que o usuário tenha dado no post anteriormente
#         PostInteraction.objects.filter(user=user, post=post, interaction_type=PostInteraction.LIKE).delete()
#         # Adiciona a descurtida
#         PostInteraction.objects.create(user=user, post=post, interaction_type=PostInteraction.DISLIKE)
#         return Response({"message": "Post descurtido com sucesso"})


# # TODO: Implementar list_all_friends_from_user passando o id do usuário desejado
# @api_view(["GET"])
# def list_all_users(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)


# # alterar os metodos, acho que nao estao funcionando :)
# @api_view(["GET"])
# def list_followed_by(request, username):
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         return Response({"message": "User not found"}, status=404)

#     followed_by = user.followed_by.all()
#     serializer = UserSerializer(followed_by, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def list_followers(request, username):
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         return Response({"message": "User not found"}, status=404)

#     followers = user.followers.all()
#     serializer = UserSerializer(followers, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def list_comments_post(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return Response({"message": "Post not found"}, status=404)

#     comments = post.comments.all()
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)


# @api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def like_post(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return Response({"message": "Post not found"}, status=404)

#     user = request.user
#     post_interaction = PostInteraction.objects.create(user=user, post=post, interaction_type=PostInteraction.LIKE)
#     serializer = PostInteractionSerializer(post_interaction)
#     return Response(serializer.data, status=201)
