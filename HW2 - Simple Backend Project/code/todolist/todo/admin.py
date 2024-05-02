from django.contrib import admin
from .models import Task

# Register your models here.
class TasksAdmin(admin.ModelAdmin):
    search_fields = ['content']

admin.site.register(Task, TasksAdmin)

