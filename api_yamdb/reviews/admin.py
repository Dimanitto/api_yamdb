from django.contrib import admin
from reviews import models


@admin.register(models.User)
class User(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
