from django.contrib import admin

from users.models import UserModel, UserConfirmModel

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_active', 'is_superuser']


admin.site.register(UserConfirmModel)
