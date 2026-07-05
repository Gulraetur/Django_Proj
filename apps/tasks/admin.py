from django.contrib import admin
from .models import Task, TaskMaterial, TaskHistory

class TaskMaterialInline(admin.TabularInline):
    model = TaskMaterial
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_filter = ("status",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = (TaskMaterialInline,)
    
@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ('task', 'from_status', 'to_status', 'changed_by', 'created_at')
    
@admin.register(TaskMaterial)
class TaskMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')