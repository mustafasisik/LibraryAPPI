from django.db import models
from django.contrib.auth.models import User


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
