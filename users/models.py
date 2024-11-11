import random
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import BaseModel

class UserRole(models.TextChoices):
    ORDINARY = 'ORDINARY', 'ordinary'
    ADMIN = 'ADMIN', 'admin'
    MANAGER = 'MANAGER', 'manager'


class AuthType(models.TextChoices):
    VIA_EMAIL = 'VIA_EMAIL', 'via_email'
    VIA_PHONE = 'VIA_PHONE', 'via_phone'


class AuthStatus(models.TextChoices):
    NEW = 'NEW', 'new'
    CODE_VERIFIED = 'CODE_VERIFIED', 'new'
    DONE = 'DONE', 'done'
    PHOTO_STEP = 'PHOTO_STEP', 'photo_step'


class UserModel(AbstractUser, BaseModel):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)

    auth_status = models.CharField(max_length=50, choices=AuthStatus.choices, default=AuthStatus.NEW)
    auth_type = models.CharField(max_length=50, choices=AuthType.choices)
    user_role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.ORDINARY)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self):
        code = "".join(str(random.randint(0, 100) // 10) for _ in range(4))

        UserConfirmModel.objects.create(
            code=code,
            user=self,
        )
        return code

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    def check_username(self):
        if not self.username:
            temp_username = f"instagram-{str(self.id).split('-')[-1]}"
            while UserModel.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username

    def save(self, *args, **kwargs):
        self.check_username()
        super(UserModel, self).save(*args, **kwargs)




class UserConfirmModel(models.Model):
    code = models.CharField(max_length=4)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verify_codes')

    def __str__(self):
        return f"{self.user.__str__()} - {self.code}"

    class Meta:
        verbose_name = 'Verification code'
        verbose_name_plural = 'Verification codes'
        unique_together = ('user', 'code')
