from django.db import models
from django.utils.text import slugify
from apps.users.models import User
    

class Task(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('search', 'Поиск исполнителя'),
        ('work', 'В работе'),
        ('delivered', 'Сдача результата'),
        ('review', 'Приём'),
        ('closed', 'Закрыт'),
        ('dispute', 'Оспаривание'),
        
    )
    
    title = models.CharField(max_length=255, verbose_name="Задача")
    slug = models.SlugField(unique=True,blank=True, verbose_name="URL-идентификатор")
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Бюджет")
    deadline = models.DateTimeField(verbose_name="Крайний срок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    
    file = models.FileField(upload_to='results/', blank=True, null=True, verbose_name="Файл задачи")
    url = models.URLField(blank=True, verbose_name="Ссылка")
    
    client = models.ForeignKey(
        User,  on_delete=models.CASCADE,
        related_name='taskrs_as_client',
        limit_choices_to={'client_profile__isnull':False},
        verbose_name="Заказчик"
    )
    
    executor = models.ForeignKey(
        User,  on_delete=models.CASCADE,
        related_name='tasks_as_executor',
        limit_choices_to={'executor_profile__isnull':False},
        verbose_name="Исполнитель",
        blank=True,
        null=True,
    )
    # result_file = models.FileField(upload_to='results/', blank=True, null=True, verbose_name="Файл результата")
    # result_comment = models.TextField(blank=True, verbose_name="Комментарий к результату")
        
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f"#{self.id} {self.title}"
    
class TaskMaterial(models.Model):
    task = models.ForeignKey(
        "tasks.Task", 
        related_name="results",
        verbose_name="Задача", 
        on_delete=models.CASCADE,
        
        )
    result_file = models.FileField(upload_to='results/', blank=True, null=True, verbose_name="Файл результата")
    url = models.URLField(blank=True, null=True, verbose_name="Ссылка")
    title = models.CharField(max_length=255, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Материал результата"
        verbose_name_plural = "Материалы результатов"
    def __str__(self):
        return f"#{self.id} {self.title}"
    
class TaskHistory(models.Model):
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history', verbose_name="Заказ")
    from_status = models.CharField(max_length=20, verbose_name="Из статуса")
    to_status = models.CharField(max_length=20, verbose_name="В статус")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Кто изменил")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = 'История заказа'
        verbose_name_plural = 'Истории заказов'
    