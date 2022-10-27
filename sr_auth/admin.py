from django.contrib import admin
from .models import Product, ProductAuth
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from guardian.admin import GuardedModelAdmin

#just use default admin for product
admin.site.register(Product)

#ProductAuth uses "object-level" permission from Guardian module, so we need to use Guardian's admin
class ProductAuthAdmin(GuardedModelAdmin):
    list_display = ('product', 'enabled', )
    search_fields = ('product', 'enabled')


admin.site.register(ProductAuth, ProductAuthAdmin)




