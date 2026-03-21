from django.contrib import admin
from .models.userprofile import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school')
    search_fields = ('user__username', 'school__name')