from django.db import models

# Create your models here.
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