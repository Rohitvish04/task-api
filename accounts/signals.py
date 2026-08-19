from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User


# bonus requirement - default every new account to USER unless a role
# was explicitly set during registration
@receiver(pre_save, sender=User)
def set_default_role(sender, instance, **kwargs):
    if not instance.role:
        instance.role = "USER"
