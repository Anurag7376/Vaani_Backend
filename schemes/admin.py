from django.contrib import admin
from .models import Scheme


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'govt_type',
        'state',
        'income_limit',
        'is_active'
    )

    list_filter = (
        'category',
        'govt_type',
        'state',
        'is_active'
    )

    search_fields = ('title', 'description')
