from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    """
    Creates a profile instance when a new user is registered.
    Updates related profile instance when a user instance is saved(changed).
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
