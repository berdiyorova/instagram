from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.utility import check_email_or_phone
from users.models import UserModel, AuthType, AuthStatus


class RegisterSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(RegisterSerializer, self).__init__(*args, **kwargs)
        self.fields['email_or_phone'] = serializers.CharField(required=False)

    class Meta:
        model = UserModel
        fields = ['id', 'auth_type', 'auth_status']
        read_only_fields = ['id', 'auth_type', 'auth_status']

    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')
        input_type = check_email_or_phone(email_or_phone)

        if input_type == 'email':
            attrs = {
                'email': email_or_phone,
                'auth_type': AuthType.VIA_EMAIL
            }
        elif input_type == 'phone':
            attrs = {
                'phone': email_or_phone,
                'auth_type': AuthType.VIA_PHONE
            }
        else:
            raise ValidationError({
                'success': False,
                'message': 'You must enter email or phone number.'
            })

        return attrs

    def validate_email_or_phone(self, value):
        if value and UserModel.objects.filter(email=value).exists():
            data = {
                'success': False,
                'message': "The email is already registered"
            }
            raise ValidationError(data)
        elif value and UserModel.objects.filter(phone=value).exists():
            data = {
                'success': False,
                'message': "The phone number is already registered"
            }
            raise ValidationError(data)
        return value


class ChangeUserInfoSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        try:
            validate_password(password=password)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return attrs

    def update(self, instance, validated_data):
        instance.first_name = self.validated_data['first_name']
        instance.last_name = self.validated_data['last_name']
        instance.username = self.validated_data['username']
        instance.set_password(self.validated_data['password'])
        instance.auth_status = AuthStatus.DONE

        instance.save()
        return instance

    def to_representation(self, instance):
        return Response(
                {
                    'success': True,
                    'message': 'User updated successfully',
                    'auth_status': instance.auth_status
                }, status=status.HTTP_202_ACCEPTED
            )
