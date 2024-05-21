from django.contrib import admin
from .models import Profile, ProfileImage


class ProfileImageInline(admin.StackedInline):
    model = ProfileImage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProfileImageInline]

    class Meta:
        model = Profile
