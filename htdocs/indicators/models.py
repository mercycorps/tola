from django.db import models
from django.contrib import admin
from silo.models import Silo
from activitydb.models import Program, Sector
from datetime import datetime



class IndicatorType(models.Model):
    indicator_type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.indicator_type


class IndicatorTypeAdmin(admin.ModelAdmin):
    list_display = ('indicator_type','description','create_date','edit_date')
    display = 'Indicator Type'


class Indicator(models.Model):
    owner = models.ForeignKey('auth.User')
    indicator_type = models.ForeignKey(IndicatorType)
    program = models.ManyToManyField(Program)
    name = models.TextField()
    sector = models.ForeignKey(Sector)
    description = models.TextField()
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        #onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Indicator, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('owner','indicator_type','name','sector','description', 'program')
    display = 'Indicators'
