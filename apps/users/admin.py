from django.contrib import admin
from .models import User, ClientProfile, ExecutorProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username', 'created_at')
    list_select_related = ('user',)
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Заказчик'

@admin.register(ExecutorProfile)
class ExecutorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_username','created_at')
    list_select_related = ('user',)
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Исполнитель'