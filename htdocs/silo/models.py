from django.db import models
from django.contrib import admin
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from oauth2client.django_orm import CredentialsField


class GoogleCredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True, related_name='google_credentials')
    credential = CredentialsField()


#READ MODELS
class ReadType(models.Model):
    read_type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.read_type


class ReadTypeAdmin(admin.ModelAdmin):
    list_display = ('read_type','description','create_date','edit_date')
    display = 'Read Type'

class Read(models.Model):
    owner = models.ForeignKey('auth.User')
    #silo = models.ManyToManyField(Silo, related_name = "reads") #RemoteEndPoint
    type = models.ForeignKey(ReadType)
    read_name = models.CharField(max_length=100, blank=True, default='', verbose_name='source name') #RemoteEndPoint = name
    description = models.TextField()
    read_url = models.CharField(max_length=100, blank=True, default='', verbose_name='source url') #RemoteEndPoint = link
    resource_id = models.CharField(max_length=200, null=True, blank=True) #RemoteEndPoint
    username = models.CharField(max_length=20, null=True, blank=True) #RemoteEndPoint
    token = models.CharField(max_length=254, null=True, blank=True) #RemoteEndPoint
    file_data = models.FileField("Upload CSV File", upload_to='uploads', blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=True)
    edit_date = models.DateTimeField(null=True, blank=True, auto_now=True, auto_now_add=False) #RemoteEndPoint
    

    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        super(Read, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.read_name


class ReadAdmin(admin.ModelAdmin):
    list_display = ('owner','read_name','read_url','description','create_date')
    display = 'Read Data Feeds'


# Create your models here.
class Silo(models.Model):
    owner = models.ForeignKey('auth.User')
    name = models.TextField()
    reads = models.ManyToManyField(Read, related_name='silos')
    description = models.TextField()
    create_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        super(Silo, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

"""
class RemoteEndPoint(models.Model):
    
    Remote_end_points are end-points that data could be exported to
    or imported from on a per silo basis.
    
    name = models.CharField(max_length=60, null=False, blank=False)
    silo = models.ForeignKey(Silo, related_name = "remote_end_points")
    link = models.URLField(null=False, blank=False)
    resource_id = models.CharField(max_length=200, null=True, blank=True)
    token = models.CharField(max_length=254, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    edit_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name
"""

class SiloAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'source', 'description', 'create_date')
    display = 'Data Feeds'
    

from mongoengine import *
class LabelValueStore(DynamicDocument):
    silo_id = IntField()
    create_date = DateTimeField(help_text='date created')
    edit_date = DateTimeField(help_text='date editted')