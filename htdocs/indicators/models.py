from django.db import models
from django.contrib import admin
from silo.models import Silo


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


class Sector(models.Model):
    sector = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.sector


class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector','description','create_date','edit_date')
    display = 'Sector'


class ActivityData(models.Model):
    url = models.CharField(max_length=765, blank=True)
    silo = models.ForeignKey(Silo)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.url


class ActivityDataAdmin(admin.ModelAdmin):
    list_display = ('url','description','create_date','edit_date')
    display = 'Activity Data'


class PeriodType(models.Model):
    type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    length = models.CharField(max_length=135, blank=True)

    def __unicode__(self):
        return self.type


class PeriodTypeAdmin(admin.ModelAdmin):
    list_display = ('type','description','length')
    display = 'Period Types'


class DisaggregationType(models.Model):
    type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)

    def __unicode__(self):
        return unicode(self.type)


class DisaggregationTypeAdmin(admin.ModelAdmin):
    list_display = ('type','description')
    display = 'Disaggregation Types'


class Program(models.Model):
    owner = models.ForeignKey('auth.User')
    grantid = models.CharField(max_length=135, blank=True)
    name = models.CharField(max_length=765, blank=True)
    sector = models.ForeignKey(Sector)
    description = models.CharField(max_length=765, blank=True)
    storagebin_url = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('grantid','name','sector','description','storagebin_url','create_date','edit_date')
    display = 'Programs'


class Indicator(models.Model):
    owner = models.ForeignKey('auth.User')
    indicator_type = models.ForeignKey(IndicatorType)
    program = models.ForeignKey(Program)
    name = models.TextField()
    activity = models.ForeignKey(ActivityData)
    sector = models.ForeignKey(Sector)
    description = models.TextField()
    create_date = models.DateTimeField(null=True, blank=True)
    target = models.CharField(max_length=135, blank=True)
    target_actual = models.CharField(max_length=135, blank=True)
    disaggregation_type = models.ManyToManyField(DisaggregationType)
    budget = models.CharField(max_length=135, blank=True)
    budget_actual = models.CharField(max_length=135, blank=True)
    period = models.ForeignKey(PeriodType)
    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        super(Indicator, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('owner','indicator_type','name','sector','activityData','description','dissaggregation_type')
    display = 'Indicators'


class TargetsAndActuals(models.Model):
    disaggregation_type = models.ForeignKey(DisaggregationType)
    period = models.ForeignKey(PeriodType)
    indicator = models.ForeignKey(Indicator)
    target_value = models.CharField(max_length=765, blank=True)
    actual_value = models.CharField(max_length=765, blank=True)

    def __unicode__(self):
        return self.disaggregation_type.type


class TargetsAndActualsAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_type','period','indicator')
    display = 'Disaggregation Types'