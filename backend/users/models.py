from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_username, validate_password


class User(AbstractUser):
    """Users model"""
    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODER, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    first_name = models.CharField('Name', max_length=150, blank=True)
    last_name = models.CharField('Surname', max_length=150, blank=True)
    email = models.EmailField('Email', unique=True, max_length=254)
    role = models.CharField(
        'Role',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER
    )
    password = models.CharField(
        'password',
        max_length=150,
        blank=True,
        validators=(validate_password,)
    )
    confirmation_code = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Identification code'
    )
    otp = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name='OTP code'
    )
    otp_date = models.DateTimeField(
        editable=True,
        verbose_name='otp_date_expired',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_together'
            )
        ]

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODER

    def __str__(self):
        return self.username
