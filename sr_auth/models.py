from django.db import models
from solo.models import SingletonModel


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            primary_key=True, help_text="Name of the product")

    def __str__(self):
        return u'%s' % (self.name)

class ProductAuth(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=False, blank=False)
    #auth enabled
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return "Product Auth Configuration"

    class Meta:
        verbose_name = "Auth Configuration"
        permissions = [
            ("can_enable_auth", "Can enable of disable authentication for this product."),
            ("can_use", "Can be authorized to use this product"),
        ]
        

