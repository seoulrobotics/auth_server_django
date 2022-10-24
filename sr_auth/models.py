from django.db import models
from django.contrib.auth.models import User


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
        return f"{self.product.name} Auth"

    # class Meta:
    #     verbose_name = "Auth Configuration"

class CanUseUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, blank=False)
    product_auth = models.ForeignKey(
        ProductAuth, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Can use {self.product_auth.product.name}"
    
    
class CanEnableAuthUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, blank=False)
    product_auth = models.ForeignKey(
        ProductAuth, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self):
        return f"Can enable authentication of {self.product_auth.product.name}"




