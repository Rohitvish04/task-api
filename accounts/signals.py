from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User


# adding this as a safety net - even if someone creates a User outside
# the serializer (shell, admin panel, whatever), they shouldn't end up
# with a blank role
@receiver(pre_save, sender=User)
def set_default_role(sender, instance, **kwargs):
    if not instance.role:
        instance.role = "USER"
