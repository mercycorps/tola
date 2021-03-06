from django.db import models
from django.contrib import admin
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from oauth2client.django_orm import CredentialsField


class GoogleCredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True, related_name='google_credentials')
    credential = CredentialsField()

class ThirdPartyTokens(models.Model):
    user = models.ForeignKey(User, related_name="tokens")
    name = models.CharField(max_length=60)
    token = models.CharField(max_length=255)
    create_date = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=True)
    edit_date = models.DateTimeField(null=True, blank=True, auto_now=True, auto_now_add=False)


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
    FREQUENCY_DAILY = 'daily'
    FREQUENCY_WEEKLY = 'weekly'
    FREQUENCY_CHOICES = (
        (FREQUENCY_DAILY, 'Daily'),
        (FREQUENCY_WEEKLY, 'Weekly'),
    )
    owner = models.ForeignKey(User)
    type = models.ForeignKey(ReadType)
    read_name = models.CharField(max_length=100, blank=True, default='', verbose_name='source name') #RemoteEndPoint = name
    autopull = models.BooleanField(default=False)
    autopull_frequency = models.CharField(max_length=25, choices=FREQUENCY_CHOICES, null=True, blank=True)
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


class Tag(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='tags')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# Create your models here.
class Silo(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length = 60, blank=False, null=False)
    reads = models.ManyToManyField(Read, related_name='silos')
    tags = models.ManyToManyField(Tag, related_name='silos', blank=True)
    shared = models.ManyToManyField(User, related_name='silos', blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    public = models.BooleanField()
    create_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        super(Silo, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @property
    def tag_list(self):
        return ', '.join([x.name for x in self.tags.all()])

class SiloAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'source', 'description', 'create_date')
    display = 'Data Feeds'


from mongoengine import *
class LabelValueStore(DynamicDocument):
    silo_id = IntField()
    create_date = DateTimeField(help_text='date created')
    edit_date = DateTimeField(help_text='date editted')


### DOCUMENTATION and HELP
# Documentation
class DocumentationApp(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)
    documentation = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(DocumentationApp, self).save()

    def __unicode__(self):
        return unicode(self.name)


class DocumentationAppAdmin(admin.ModelAdmin):
    list_display = ('name', 'documentation', 'create_date',)
    display = 'DocumentationApp'


# collect feedback from users
class Feedback(models.Model):
    submitter = models.ForeignKey(User)
    note = models.TextField()
    page = models.CharField(max_length=135)
    severity = models.CharField(max_length=135)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(Feedback, self).save()

    def __unicode__(self):
        return unicode(self.submitter)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('submitter', 'note', 'page', 'severity', 'create_date',)
    display = 'Feedback'


# FAQ
class FAQ(models.Model):
    question = models.TextField(null=True, blank=True)
    answer =  models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(FAQ, self).save()

    def __unicode__(self):
        return unicode(self.question)


class FAQAdmin(admin.ModelAdmin):
    list_display = ( 'question', 'answer', 'create_date',)
    display = 'FAQ'