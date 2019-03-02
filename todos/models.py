import datetime

from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Todo(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)
    description = models.TextField(blank=False, null=False)
    completed = models.BooleanField(blank=False, null=False, default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.created_at is None:
            self.created_at = datetime.datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.datetime.now()

        return super(Todo, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                      update_fields=update_fields)


@receiver(post_save, sender=Todo)
def update_date(sender, **kwargs):
    # only on update
    if not kwargs.get('created', False):
        sender.updated_at = datetime.datetime.now()
