from django.contrib import admin

from .models import Stat


class StatAdmin(admin.ModelAdmin):
    list_display = (
        'ap',
        'max',
        'current',
        'min',
        'avg',
        'timestamp',
    )


admin.site.register(Stat, StatAdmin)
