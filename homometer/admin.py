from django.contrib import admin

from .models import Stat


class StatAdmin(admin.ModelAdmin):
    list_display = (
        'ap',
        'current',
        'timestamp',
    )


admin.site.register(Stat, StatAdmin)
