from django.db import models
from django.contrib import admin
from django.conf import settings
from datetime import datetime
from read.models import Read

#Programs
class Program(models.Model):
    name = models.CharField("Program Name", max_length=255, blank=True)
    description = models.CharField("Program Description", max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Program, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


#Programs Admin Interface
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Program'


#Countires
class Country(models.Model):
    country = models.CharField("Country Name", max_length=255, blank=True)
    code = models.CharField("2 Letter Country Code", max_length=4, blank=True)
    description = models.CharField("Description/Notes", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('country',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Country, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.country


#Country Admin Interface
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Country'


#Province
class Province(models.Model):
    name = models.CharField("Province Name", max_length=255, blank=True)
    country = models.ForeignKey(Country)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Province, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


#Province Admin Interface
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date', 'edit_date')
    display = 'Province'


#District
class District(models.Model):
    name = models.CharField("District Name", max_length=255, blank=True)
    province = models.ForeignKey(Province)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(District, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


#District Admin Interface
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'create_date', 'edit_date')
    display = 'District'

#Cluster
class Cluster(models.Model):
    name = models.CharField("Cluster Name", max_length=255, blank=True)
    district = models.ForeignKey(District)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Cluster, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


#Cluster Admin Interface
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date', 'edit_date')
    display = 'Cluster'


#Village
class Village(models.Model):
    name = models.CharField("Village Name", max_length=255, blank=True)
    district = models.ForeignKey(District)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Village, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


#Village Admin Interface
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date', 'edit_date')
    display = 'Village'


# Project Proposal Form
class ProjectProposal(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True)
    profile_code = models.CharField("Profile Code", max_length=255, blank=True)
    proposal_num = models.CharField("Proposal Number", max_length=255, blank=True)
    date_of_request = models.DateTimeField("Date of Request", null=True, blank=True)
    project_title = models.CharField("Project Title", max_length=255, blank=True)
    project_type = models.CharField("Proposal Number", max_length=255, blank=True)
    country = models.ForeignKey(Country)
    province = models.ForeignKey(Province, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True)
    village = models.ForeignKey(Village, null=True, blank=True)
    cluster = models.ForeignKey(Cluster, null=True, blank=True)
    community_rep = models.CharField("Community Representative", max_length=255, blank=True)
    community_rep_contact = models.CharField("Community Representative Contact", max_length=255, blank=True)
    community_mobilizer = models.CharField("Community Mobilizer", max_length=255, blank=True)
    prop_status = models.CharField("Proposal Status", max_length=255, blank=True)
    rej_letter = models.TextField("Rejection Letter", blank=True)
    project_code = models.CharField("Project Code", max_length=255, blank=True)
    project_description = models.TextField("Project Description", blank=True)
    approval = models.BooleanField("Approval", default="0")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="approving")
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="requesting")
    approval_remarks = models.CharField("Approval Remarks", max_length=255, blank=True)
    device_id = models.CharField("Device ID", max_length=255, blank=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    proposal_review = models.FileField("Proposal Review", upload_to='uploads', blank=True, null=True)
    proposal_review_2 = models.FileField("Proposal Review Additional", upload_to='uploads', blank=True, null=True)
    today = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    meta_instance_id = models.CharField("Meta Instance ID", max_length=255, blank=True)
    meta_instance_name = models.CharField("Meta Instance Name", max_length=255, blank=True)
    odk_id = models.CharField("ODK ID", max_length=255, blank=True)
    odk_uuid = models.CharField("ODK UUID", max_length=255, blank=True)
    odk_submission_time = models.DateTimeField("ODK Submission Time", null=True, blank=True)
    odk_index = models.CharField("ODK Index", max_length=255, blank=True)
    odk_parent_table_name = models.CharField("ODK Table Name", max_length=255, blank=True)
    odk_tags = models.CharField("ODK Tags", max_length=255, blank=True)
    odk_notes = models.CharField("ODK Notes", max_length=255, blank=True)
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)
    latitude = models.CharField("Latitude (Coordinates)", max_length=255, blank=True)
    longitude = models.CharField("Longitude (Coordinates)", max_length=255, blank=True)


    class Meta:
        ordering = ('create_date',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectProposal, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.project_title

#Dashboard
class ProgramDashboard(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True)
    project_proposal = models.IntegerField(null=True,blank=True)
    project_proposal_approved = models.IntegerField(null=True,blank=True)
    project_agreement = models.IntegerField(null=True,blank=True)
    project_agreement_approved = models.IntegerField(null=True,blank=True)
    project_completion = models.IntegerField(null=True,blank=True)
    project_completion_approved = models.IntegerField(null=True,blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('program',)

    #onsave add create date or update edit date
    def save(self):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProgramDashboard, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return unicode(self.program)


#District Admin Interface
class ProgramDashboardAdmin(admin.ModelAdmin):
    list_display = ('program', 'project_proposal', 'project_proposal_approved', 'create_date', 'edit_date')
    display = 'Program Dashboard'


#Merge Map
class MergeMap(models.Model):
    read = models.ForeignKey(Read, null=False, blank=False)
    project_proposal = models.ForeignKey(ProjectProposal, null=False, blank=False)
    from_column = models.CharField(max_length=255, blank=True)
    to_column = models.CharField(max_length=255, blank=True)


class MergeMapAdmin(admin.ModelAdmin):
    list_display = ('read', 'project_proposal', 'from_column', 'to_column')
    display = 'project_proposal'


