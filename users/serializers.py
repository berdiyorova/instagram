from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.utility import check_email_or_phone
from users.models import UserModel, AuthType


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
