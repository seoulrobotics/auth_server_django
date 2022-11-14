from django.apps import AppConfig




def init_settings(init_configs):
    from django.contrib.auth.models import User
    from .models import ProductAuth
    from guardian.shortcuts import assign_perm
    # #TODO: currently this is a solution to enable authentication with access to user management UI.
    default_users = init_configs["DEFAULT_PRODUCT_USERS"]
    for product_name, password in default_users.items():
        product_auth = ProductAuth.objects.get(product=product_name)
        default_username = f'{product_name}_default_user'
        #remove existing default user
        try:
            existing = User.objects.get(username = default_username)
            existing.delete()
        except:
            pass
        #add new default user with new password
        user=User.objects.create_user(default_username, password=password)
        
        user.is_superuser=False
        user.is_staff=False
        user.save()
        assign_perm('can_use', user, product_auth)
        assign_perm('can_enable_auth', user, product_auth)
        
        
        
            

class SRAuthServiceConfig(AppConfig):
    name = 'sr_auth'
    def ready(self):
        from .init_settings import get_configs
        init_settings(get_configs())

            
        
        

        

