from django.db import models
from django.db.models import CASCADE
from django.utils import timezone
from django.utils.crypto import get_random_string
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Token(models.Model):
    key = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey('users.User', CASCADE, 'tokens')
    expires_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    @classmethod
    def create_token_for_user(cls, user):
        token = get_random_string(length=40)
        return cls.objects.create(key=token, user=user)

    class Meta:
        db_table = 'users_tokens'
