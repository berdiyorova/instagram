from django.contrib import admin

from users.models import UserModel, UserConfirmModel

admin.site.register(UserModel)
admin.site.register(UserConfirmModel)
