from django.contrib import admin
from .models import Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'executor', 'proposed_price', 'status', 'created_at')
    list_filter = ('status',)