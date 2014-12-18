from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from oPOSum.apps.branches.models import Branch
# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User)
    branch = models.ManyToManyField(Branch, blank=True)

    def __unicode__(self):
        return "%s's Account" % (self.user)

def create_employee(sender, instance, created, **kwargs):
    if created:
        profile, created = Employee.objects.get_or_create(user=instance)

post_save.connect(create_employee, sender=User)
