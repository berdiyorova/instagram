from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from common.utility import check_email_or_phone, check_user_type
from users.models import UserModel, AuthType, AuthStatus, FollowingModel


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

    def to_representation(self, instance):
        data = super(RegisterSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class ChangeUserInfoSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        if password:
            try:
                validate_password(password=password)
            except Exception as e:
                raise serializers.ValidationError(str(e))

        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('confirm_password'):
            validated_data.pop('confirm_password')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if validated_data.get('password'):
            instance.set_password(self.validated_data['password'])

        if instance.auth_status == AuthStatus.CODE_VERIFIED:
            instance.auth_status = AuthStatus.DONE

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['success'] = True
        representation['message'] = 'User updated successfully'
        representation['auth_status'] = instance.auth_status
        return representation


class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True)

    def validate(self, attrs):
        user_input = attrs.get('user_input')
        password = attrs.get('password')
        user_type = check_user_type(user_input)
        user = None

        if user_type == 'email':
            user = UserModel.objects.get(email=user_input)
        elif user_type == 'phone':
            user = UserModel.objects.get(phone=user_input)
        elif user_type == 'username':
            user = UserModel.objects.get(username=user_input)

        if user is not None and user.auth_status == AuthStatus.NEW:
            raise PermissionDenied("You are not fully registered.")

        authenticated_user = authenticate(username=user.username, password=password)
        if not authenticated_user:
            raise serializers.ValidationError("Email/Username/Phone_number or password is not valid")

        attrs = user.token()
        attrs['auth_status'] = user.auth_status
        attrs['full_name'] = user.full_name
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)


class FollowingSerializer(serializers.ModelSerializer):
    to_user = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())

    class Meta:
        model = FollowingModel
        fields = ['to_user', 'created_at']
