from django.db import models


class Scheme(models.Model):

    CATEGORY_CHOICES = (
        ('education', 'Education'),
        ('health', 'Health'),
        ('agriculture', 'Agriculture'),
        ('employment', 'Employment'),
        ('housing', 'Housing'),
        ('women', 'Women Empowerment'),
        ('startup', 'Startup'),
        ('pension', 'Pension'),
    )

    GOVT_TYPE = (
        ('central', 'Central Government'),
        ('state', 'State Government'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    income_limit = models.FloatField(null=True, blank=True)

    residence_type = models.CharField(
        max_length=10,
        choices=[('urban', 'Urban'), ('rural', 'Rural')],
        null=True,
        blank=True
    )

    eligible_categories = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )  # general/obc/sc/st

    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)

    state = models.CharField(max_length=100, null=True, blank=True)

    govt_type = models.CharField(max_length=20, choices=GOVT_TYPE)

    official_link = models.URLField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
