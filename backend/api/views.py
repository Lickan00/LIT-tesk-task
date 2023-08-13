import uuid
import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, AllowAny
)
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (UserSerializer, SignupSerializer, LoginSerializer,
                          OtpSerializer)
from .permissions import IsAuthorOrModeratorOrReadOnly
from .utils import send_otp_email
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for UserSerializer."""
    queryset = User.objects.all()
    permission_classes = (IsAuthorOrModeratorOrReadOnly,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')

    # @action(
    #     detail=False,
    #     methods=('GET', 'PATCH'),
    #     url_path='me',
    #     permission_classes=(IsAuthenticated,),
    #     serializer_class=UserSerializer
    # )
    # def me(self, request):
    #     user = get_object_or_404(User, pk=request.user.id)
    #     serializer = self.get_serializer(
    #         user, data=request.data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(role=user.role)

    #     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Authorization method by sending a letter."""
    serializer = SignupSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email'),
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    serializer.validated_data['password'] = make_password(
        request.data['password']
    )
    try:
        user, created = User.objects.get_or_create(
            **serializer.validated_data,
            confirmation_code=confirmation_code,
        )
    except Exception as error:
        return Response(
            f'Получена ошибка ->{error}<-',
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    password = serializer.validated_data['password']
    user_obj = User.objects.filter(email=email)
    if not user_obj.exists():
        return Response(
            'Incorrect Email', status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, email=email)
    if not check_password(password, user.password):
        return Response(
            'Incorrect password', status=status.HTTP_400_BAD_REQUEST
        )
    send_otp_email.delay(email)

    return Response(
        'Check your email, we send OTP code',
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify(request):
    serializer = OtpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    otp = serializer.validated_data['otp']
    email = serializer.validated_data['email']
    user = User.objects.filter(email=email)
    if not user.exists():
        return Response(
            'Incorrect Email', status=status.HTTP_400_BAD_REQUEST
        )
    user_obj = get_object_or_404(User, email=email)
    if user_obj.otp != otp:
        return Response(
            'Incorrect OTP code', status=status.HTTP_400_BAD_REQUEST
        )
    current_dt = datetime.datetime.now() - datetime.timedelta(minutes=1)
    if user_obj.otp_date < current_dt:
        return Response(
            'OTP code has expired, please request a new code',
            status=status.HTTP_400_BAD_REQUEST
        )
    refresh = RefreshToken.for_user(user_obj)
    token_data = {'token': str(refresh.access_token)}

    return Response(token_data, status=status.HTTP_200_OK)
