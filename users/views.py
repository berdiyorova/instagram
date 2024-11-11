from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utility import check_email_or_phone, send_verify_code_to_email, send_verify_code_to_phone
from users.models import UserModel, AuthStatus
from users.serializers import RegisterSerializer


PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny,]


class VerifyView(APIView):
    def post(self, *args, **kwargs):
        user_input = self.request.data.get('email_or_phone')
        code = self.request.data.get('code')
        input_type = check_email_or_phone(user_input)

        user = UserModel.objects.filter(Q(email=user_input) | Q(phone=user_input)).first()

        if user:
            self.check_verify(user, code, input_type)

            return Response(
                data={
                    'success': True,
                    'auth_status': user.auth_status,
                    'message': f"Your {input_type} has been verified."
                }, status=status.HTTP_200_OK
            )

        else:
            return Response(
                data={
                    'success': False,
                    'message': 'User not fount.'
                }, status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def check_verify(user, code, input_type):
        if input_type == 'email':
            expiration_time = EMAIL_EXPIRE
        else:
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
            user.auth_status = AuthStatus.CODE_VERIFIED
            user.save()

        return True


class ResendVerifyView(APIView):
    def post(self, *args, **kwargs):
        user_input = self.request.data.get('email_or_phone')
        input_type = check_email_or_phone(user_input)
        user = UserModel.objects.filter(Q(email=user_input) | Q(phone=user_input)).first()

        self.check_verification(user=user, input_type=input_type)
        code = user.create_verify_code()

        if input_type == 'email':
            send_verify_code_to_email(user.email, code)

        elif input_type == 'phone':
            send_verify_code_to_phone(user.phone, code)

        return Response(
            data={
                'success': True,
                'message': 'Your verification code has been resent.'
            }, status=status.HTTP_200_OK
        )

    @staticmethod
    def check_verification(user, input_type):
        if input_type == 'email':
            expiration_time = EMAIL_EXPIRE
        else:
            expiration_time = PHONE_EXPIRE

        verifies = user.verify_codes.filter(
            created_at__gte=timezone.now() - timedelta(minutes=expiration_time),
            is_confirmed=False)

        if verifies.exists():
            data = {
                "message": "Your code is still usable. Wait a moment."
            }
            raise ValidationError(data)
