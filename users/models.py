from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save


# Create your models here.


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = models.CharField(blank=True, max_length=255)
    picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)

    about = models.CharField(max_length=1000, blank=True, null=True)
    rating = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.name:
            return self.name

        return self.username


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    user_email = instance.email
    username = user_email[:30]
    n = 1
    while User.objects.exclude(pk=instance.pk).filter(username=username).exists():
        n += 1
        username = user_email[:(29 - len(str(n)))] + '-' + str(n)
    instance.username = username