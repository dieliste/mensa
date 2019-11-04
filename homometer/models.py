from django.db import models
from django.utils.translation import gettext_lazy as _


class Stat(models.Model):
    ap = models.CharField(
        _('ap'),
        max_length=63,
        unique=True,
    )

    current = models.PositiveIntegerField(
        _('current'),
    )

    timestamp = models.DateTimeField(
        _('timestamp'),
        auto_now=True,
    )

    def __str__(self):
        return self.ap
