from django.shortcuts import render
from rest_framework.views import APIView

from social_network.models import Post, User
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from social_network.serializers import PostSerializer, UserSerializer

class ListPost(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
