from django.db import models
from apps.users.models import User
from apps.tasks.models import Task

class Response(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Рассматривается'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='responses')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses',
                                 limit_choices_to={'executor_profile__isnull': False})
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    proposed_deadline = models.DateTimeField()
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'