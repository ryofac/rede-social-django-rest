from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from social_network.models import User
from social_network.serializers import UserSerializer


class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=["GET"], detail=False, name="me", permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        user_data = serializer.data
        return Response(user_data)
