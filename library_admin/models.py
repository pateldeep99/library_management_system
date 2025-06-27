from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class LibraryAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_contact = models.CharField(max_length=15)
    admin_address = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Admin: {self.user.username}"