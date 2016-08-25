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
    details = models.ManyToManyField(BranchDetail, blank = True)
    ticket_pre = models.TextField(blank=True, null=True)
    ticket_post = models.TextField(blank=True, null=True)
    type = models.ForeignKey(BranchType)

    def __unicode__(self):
        return u'%s' % (self.name)

    def as_json(self):
        ret = dict(
            slug = self.slug,
            name = self.name,
        )
        if not self.ticket_pre is None:
            ticket_pre = self.ticket_pre.encode('utf-8'),
        else:
            ticket_pre = ""
        if not self.ticket_post is None:
            ticket_post = self.ticket_post.encode('utf-8')
        else:
            ticket_post = ""
        ret['ticket_pre'] = ticket_pre
        ret['ticket_post'] = ticket_post
        return ret
