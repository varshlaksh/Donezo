from django.contrib import admin
from .models import Task, Notification

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'deadline', 'created_by', 'assigned_to')
    list_filter = ('status', 'priority', 'created_by', 'assigned_to')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    ordering = ('-created_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'message', 'timestamp', 'is_read')
    list_filter = ('is_read', 'user')
    search_fields = ('message', 'user__username')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
