from django.db import models

# Create your models here.

class BranchDetail(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255,blank=False)

    def __unicode__(self):
        return u'%s : %s' % (self.name, self.description)

class BranchType(models.Model):
    name = models.CharField(max_length=255, blank=False, default="branch type", unique=True)
    description = models.CharField(max_length=255, blank=False, default="type description")

    def __unicode__(self):
        return u'%s' % (self.name)

class Branch(models.Model):
    slug = models.CharField(max_length=50, blank=False, default="branch", primary_key=True, unique=True)
    name = models.CharField(max_length=50, blank=False, default="branch name")
    address = models.CharField(max_length=255, blank=True, null=True)
    details = models.ManyToManyField(BranchDetail, null = True, blank = True)
    ticket_pre = models.TextField(max_length=255, blank=True, null=True)
    ticket_post = models.TextField(max_length=255, blank=True, null=True)
    type = models.ForeignKey(BranchType)

    def __unicode__(self):
        return u'%s' % (self.name)
