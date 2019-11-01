from django.db import models
from django.utils.translation import gettext_lazy as _


class Stat(models.Model):
    ap = models.CharField(
        _('ap'),
        max_length=63,
        unique=True,
    )

    max = models.PositiveIntegerField(
        _('max'),
    )

    current = models.PositiveIntegerField(
        _('current'),
    )

    min = models.PositiveIntegerField(
        _('min'),
    )

    avg = models.DecimalField(
        _('avg'),
        max_digits=5,
        decimal_places=2,
    )

    timestamp = models.DateTimeField(
        _('timestamp'),
        auto_now=True,
    )

    def __str__(self):
        return self.ap
