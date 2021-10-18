from django.contrib import admin

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'tg_login', 'name', 'phone_number', 'answer']
    list_editable = ('name', 'phone_number', 'answer')
