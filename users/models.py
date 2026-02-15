from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    RESIDENCE_CHOICES = (
        ('urban', 'Urban'),
        ('rural', 'Rural'),
    )

    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('obc', 'OBC'),
        ('sc', 'SC'),
        ('st', 'ST'),
    )

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    residence_type = models.CharField(
        max_length=10,
        choices=RESIDENCE_CHOICES,
        null=True,
        blank=True
    )
    income = models.FloatField(null=True, blank=True)
    job_field = models.CharField(max_length=255, null=True, blank=True)
    scheme_category_interest = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True
    )
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username
