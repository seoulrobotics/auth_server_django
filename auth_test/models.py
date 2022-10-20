from django.db import models
from solo.models import SingletonModel


class AuthConfiguration(SingletonModel):
    web_auth_enabled = models.BooleanField(default=False)

    def __str__(self):
        return "Auth Configuration"

    class Meta:
        verbose_name = "Auth Configuration"
