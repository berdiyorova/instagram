from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from common.utility import check_email_or_phone, send_verify_code_to_email, send_verify_code_to_phone
from users.models import UserModel, AuthStatus, AuthType, FollowingModel
from users.serializers import RegisterSerializer, ChangeUserInfoSerializer, LoginSerializer, LogoutSerializer, \
    FollowingSerializer

PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny,]


class VerifyView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)

        return Response(
            data={
                'success': True,
                'auth_status': user.auth_status,
                'access': user.token()['access_token'],
                'refresh': user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_verify(user, code):
        if user.auth_type == AuthType.VIA_EMAIL:
            expiration_time = EMAIL_EXPIRE
        elif user.auth_type == AuthType.VIA_PHONE:
            expiration_time = PHONE_EXPIRE

        verifies = user.verify_codes.filter(
            created_at__gte=timezone.now() - timedelta(minutes=expiration_time),
            code=code,
            is_confirmed=False)

        if not verifies.exists():
            data = {
                'success': False,
                'message': 'Your verification code is incorrect or out of date.'
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
            if user.auth_status == AuthStatus.NEW:
                user.auth_status = AuthStatus.CODE_VERIFIED
            user.save()

        return True


class ResendVerifyView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, *args, **kwargs):
        user = self.request.user

        self.check_verification(user=user)
        code = user.create_verify_code()

        if user.auth_type == AuthType.VIA_EMAIL:
            send_verify_code_to_email(user.email, code)
        elif user.auth_type == AuthType.VIA_PHONE:
            send_verify_code_to_phone(user.phone, code)

        return Response(
            data={
                'success': True,
                'message': 'Your verification code has been resent.'
            }, status=status.HTTP_200_OK
        )

    @staticmethod
    def check_verification(user):
        if user.auth_type == AuthType.VIA_EMAIL:
            expiration_time = EMAIL_EXPIRE
        elif user.auth_type == AuthType.VIA_PHONE:
            expiration_time = PHONE_EXPIRE

        verifies = user.verify_codes.filter(
            created_at__gte=timezone.now() - timedelta(minutes=expiration_time),
            is_confirmed=False)

        if verifies.exists():
            data = {
                "message": "Your code is still usable. Wait a moment."
            }
            raise ValidationError(data)


class ChangeUserInformationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeUserInfoSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']

        token = RefreshToken(refresh)
        token.blacklist()

        return Response({
                'success': True,
                'message': 'You are logged out'
            }, status=status.HTTP_205_RESET_CONTENT
        )


class FollowingView(APIView):
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        to_user = serializer.validated_data['to_user']

        if user == to_user:
            raise ValidationError("You cannot follow yourself")

        data = {"success": True}
        following = FollowingModel.objects.filter(user=user, to_user=to_user)

        if following.exists():
            following.delete()
            data["message"] = f"You have unfollowed to {to_user} successfully."

            return Response(data=data, status=status.HTTP_204_NO_CONTENT)

        FollowingModel.objects.create(user=user, to_user=to_user)
        data["message"] = f"You have followed to {to_user} successfully."

        return Response(data=data, status=status.HTTP_201_CREATED)
