from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from . import serializers
from .permissions import IsAdminOrSuperuser

User = get_user_model()


class SignupView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)

        self.send_confirmation_code(request, user)
        return Response(serializer.data)

    def send_confirmation_code(self, request, username):
        email = request.data.get('email')
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Confirmation code',
            f'{confirmation_code}',
            f'{settings.ADMIN_EMAIL}',
            [f'{email}'],
            fail_silently=False,
        )


class ConfirmationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        confirmation_code = request.data.get('confirmation_code')
        username = request.data.get('username')
        serializer = serializers.ConfirmationCodeSerializer(
            data=self.request.data
        )
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(
            user, confirmation_code
        ):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'confirmation_code is uncorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.CustomUserSerializer
    permission_classes = (IsAdminOrSuperuser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = serializers.CustomUserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = get_object_or_404(User, username=self.request.user)
        serializer = serializers.CustomUserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data)
