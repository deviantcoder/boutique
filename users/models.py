from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=250, null=True, blank=True)

    image = models.ImageField(default='profile_images/profile_default.png', upload_to='profile_images')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.username


class ProfileImage(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_default.png', upload_to='profile_images')

    # def __str__(self) -> str:
    #     return self.profile.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image) as img:
            width, height = img.size
            min_side = min(img.size)

            left = (width - min_side) // 2
            top = (height - min_side) // 2
            right = (width + min_side) // 2
            bottom = (height + min_side) // 2

            img = img.crop((left, top, right, bottom))

            img.save(self.image.path, quality=50, optimize=True)
