from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User



@receiver(pre_save, sender=User)
def set_default_role(sender, instance, **kwargs):
    if not instance.role:
        instance.role = "USER"
