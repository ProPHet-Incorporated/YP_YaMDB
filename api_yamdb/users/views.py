from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.validators import ValidationError

from api.permissions import IsAdminOnly
from users.serializers import (ConfirmationCodeSerializer, MeSerializer,
                               SignUpSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Доступ: Админ
    АПИ-запросы:
    -список юзеров - GET: /users/
    -информация о юзере - GET: /users/username/
    -создание юзера - POST: /users/
    -изменение - PATCH: /users/username/
    """
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def perform_create(self, serializer):
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        if not User.objects.filter(username=username, email=email).exists():
            if User.objects.filter(email=email).exists():
                raise ValidationError(f'{username} - уже занят.')
            if User.objects.filter(username=username).exists():
                raise ValidationError(f'{email} - уже занят.')
            User.objects.create(username=username, email=email)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetriveUpdateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    pass


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Вью-функция для регистрации юзера,
    генерации кода подтверждения и
    отправки его на указанный Email.
    """
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    user, _ = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'Регистрация на YAMDB',
        (
            f'Здравствуйте, {user.username}! '
            f'Ваш код подтверждения: {confirmation_code}'
        ),
        settings.EMAIL_FOR_AUTH,
        [user.email],
        fail_silently=True,
    )
    return Response(
        {'email': user.email, 'username': user.username},
        status=status.HTTP_200_OK
    )


def get_tokens_for_user(user):
    access = AccessToken.for_user(user)

    return {
        'access': str(access),
    }


class ConfirmationCodeView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)

        confirmation_code = serializer.validated_data['confirmation_code']

        if default_token_generator.check_token(
            user,
            token=confirmation_code
        ):
            token = str(AccessToken.for_user(user))
            data = {
                'token': token['access']
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            'Неверный код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )
