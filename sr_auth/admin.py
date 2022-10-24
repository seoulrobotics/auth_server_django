from django.contrib import admin
from .models import Product, ProductAuth, CanUseUser, CanEnableAuthUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# @admin.register(CanUseUser)
# class CanUseUserAdmin(admin.ModelAdmin):
    # list_display = ['name']
    # list_filter = ['name']



# @admin.register(CanEnableAuthUser)
# class SerialBatchInstanceAdmin(admin.ModelAdmin):
    # list_display = ['product', 'enabled']
    # list_filter = ['product', 'enabled']


# admin.site.register(Product)
# # admin.site.register(ProductAuth)
admin.site.register(CanUseUser)
admin.site.register(CanEnableAuthUser)

class CanUseUserInline(admin.StackedInline):
    model = CanUseUser
    verbose_name_plural = 'Use permissions'
    can_delete = False
    def get_string(self, obj):
      if obj:
          return str(obj)
      return ""

class CanEnableAuthUserInline(admin.StackedInline):
    model = CanEnableAuthUser
    verbose_name_plural = 'Can enable auth permissions'
    can_delete = False
    def get_string(self, obj):
      if obj:
          return str(obj)
      return ""
  

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = ('product_name',) + BaseUserAdmin.list_display
    fields = ('product_name',)
    # fieldsets = ((None, {
    #     'fields': ('product_name',)
    # }),) + BaseUserAdmin.fieldsets

    
    def product_name(self, product_serial):
      return "Hello!"
    

    # def can_user(self, obj):
    #   return CanUseUserInline.get_string(self, obj.batch)
    
    # def can_enable_auth(self, obj):
    #   return SerialBatchInline.tag_list(self, obj.batch)

  # inlines = (CanUseUserInline, CanEnableAuthUserInline)
  
  # def get_form(self, request, obj=None, **kwargs):
  #     form = super(UserAdmin, self).get_form(
  #         request, obj, **kwargs)
  #     form.base_fields['batch'].label_from_instance = lambda obj: "{}".format(
  #         obj.name)
  #     return form


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



