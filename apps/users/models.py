from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=32, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="users/avatars/", blank = True, verbose_name="Аватарка")
    
    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class ClientProfile(models.Model):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="client_profile",
        verbose_name="Заказчик"   
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    class Meta:
        verbose_name = 'Профиль заказчика'
        verbose_name_plural = 'Профили заказчиков'
        
    def __str__(self):
        return self.user.get_full_name()
    
class ExecutorProfile(models.Model):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="executor_profile",
        verbose_name="Исполнитель"   
    )
    bio = models.TextField(blank=True, verbose_name="О себе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    class Meta:
        verbose_name = 'Профиль исполнителя'
        verbose_name_plural = 'Профили исполнителей'
        
    def __str__(self):
        return self.user.get_full_name()