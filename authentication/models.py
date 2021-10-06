from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from core.models import CommonFieldsMixin
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class User(AbstractUser, CommonFieldsMixin):
        def create_superuser(self, username, email, password=None):

            if password is None:
                raise TypeError("User should have a password")

            user = self.create_user(username,email, password)
            user.is_superuser =  True
            user.is_staff = True
            user.save()
            return user

        """ Base class for all users """
        is_active = models.BooleanField(default=True)
        is_verified = models.BooleanField(default=False)

        class Types(models.TextChoices):
            """ User Types """
            DONOR = "DONOR", "Donor"
            HOSPITAL = "HOSPITAL", "Hospital"
            ADMIN = "ADMIN", "Admin"

        base_type = Types.ADMIN
        type = models.CharField(_("Type"), max_length=50, choices=Types.choices, default=base_type)
        email = models.CharField(_("email of User"), unique=True, max_length=255)

        def save(self, *args, **kwargs):
            if not self.pk:
                self.type = self.base_type
                return super().save(*args, kwargs)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username']

        def tokens(self):
            refresh = RefreshToken.for_user(self)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        
        
""" ========================= Proxy Model Managers =================== """


class DonorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.DONOR)


class HospitalManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.HOSPITAL)


""" ========================== Proxy Models ============================== """


class Donor(User):
    """Class to create Gamer Object & Associated attributes """
    base_type = User.Types.DONOR
    objects = DonorManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.DONOR
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True
        ordering = ['-created_at', '-updated_at']


class Hospital(User):
    """ class to create Developer object & associated attributes """
    base_type = User.Types.HOSPITAL
    objects = HospitalManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.HOSPITAL
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        proxy = True
        ordering = ['-created_at', '-updated_at']


@receiver(post_save, sender=Donor)
@receiver(post_save, sender=Hospital)
def create_user_profile(sender, instance, created, **kwargs):
    from authentication.models import Profile
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Donor)
@receiver(post_save, sender=Hospital)
def create_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=1000)


class CustomManager(models.Manager):
    """
    Filter not return deleted objects
    """

    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(deleted=False, is_active=True)


class CommonFieldsMixin(models.Model):
    """
    Contains Common fields for every model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False,
                                  help_text="This is for soft delete")
    is_active = models.BooleanField(default=True)
    # everything will be used to query deleted objects e.g Model.everything.all()
    everything = models.Manager()
    objects = CustomManager()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.is_active = False
        self.save()

    class Meta:
        ordering = ['-updated_at', '-created_at']
        abstract = True