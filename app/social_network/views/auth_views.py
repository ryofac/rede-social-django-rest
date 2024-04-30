from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from social_network.models import User
from social_network.serializers import UserLoginSerializer, UserSerializer


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


"""
test_token: endpoint que serve somente para indicar se o token de autenticação de usuário está funcionando
"""


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    serializer = UserSerializer(request.user)
    token = Token.objects.get(user=request.user)
    return Response({"detail": "Authenticated", "token": token.key, "user": serializer.data})
