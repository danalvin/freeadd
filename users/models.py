from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.urls import reverse
from users.managers import UserManager
import uuid, base64
from django.utils.translation import ugettext_lazy as _
# from django.db.models.signals import post_save


# Create your models here.


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    username = models.CharField(blank=True, max_length=90, unique=True)
    phone = models.PositiveIntegerField(null=False, blank=False, unique=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=1000, blank=True, null=True)
    rating = models.PositiveIntegerField(null=True)
    referral_code = models.CharField(max_length=300, default='', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.username:
            return self.username

        return self.username

    def generate_verification_code(self):
        return base64.urlsafe_b64encode(uuid.uuid1().bytes)[:25]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.referral_code = self.generate_verification_code()
        elif not self.referral_code:
            self.referral_code = self.generate_verification_code()

        return super(User, self).save(*args, **kwargs)
    
    objects = UserManager()


class UserReferral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="referrer")
    referred = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="referred")

    class Meta:
        unique_together = (('referrer', 'referred'))