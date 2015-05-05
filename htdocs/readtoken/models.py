from django.db import models
from django.contrib import admin
from silo.models import Read




class Token(models.Model):
    read = models.ForeignKey(Read)
    read_token = models.CharField(max_length=100, blank=True, default='')
    read_secret = models.CharField(max_length=100, blank=True, default='')
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        super(Token, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.read_token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('read', 'read_token', 'read_secret', 'create_date')
    display = 'Read Token Auth Data Feeds'
