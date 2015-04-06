from django.db import models
from django.contrib import admin
from read.models import Read

# Create your models here.
class Silo(models.Model):
    owner = models.ForeignKey('auth.User')
    name = models.TextField()
    source = models.ForeignKey(Read)
    description = models.TextField()
    create_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        super(Silo, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class RemoteEndPoint(models.Model):
    """
    Remote_end_points are end-points that data could be exported to
    or imported from on a per silo basis.
    """
    name = models.CharField(max_length=60, null=False, blank=False)
    silo = models.ForeignKey(Silo, related_name = "remote_end_points")
    link = models.URLField(null=False, blank=False)
    token = models.CharField(max_length=254, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    edit_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name

class SiloAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'source', 'description', 'create_date')
    display = 'Data Feeds'


class DataField(models.Model):
    silo = models.ForeignKey(Silo)
    original_name = models.CharField(max_length=765, blank=True)
    name = models.CharField(max_length=765, blank=True)
    is_uid = models.NullBooleanField(null=True,blank=True)
    published = models.BooleanField(default="0")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class DataFieldAdmin(admin.ModelAdmin):
    list_display = ('silo','name','is_uid','create_date','edit_date')
    display = 'Data Fields'


class ValueStore(models.Model):
    field = models.ForeignKey(DataField)
    char_store = models.CharField(null=True, blank=True,max_length=1000)
    row_number = models.IntegerField(max_length=10, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    #set the label based on the type of value store
    def __unicode__(self):
        return self.char_store


class ValueStoreAdmin(admin.ModelAdmin):
    list_display = ('field', 'char_store', 'create_date', 'edit_date')
    display = 'Stored Values'
