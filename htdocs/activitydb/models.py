from django.db import models
from django.contrib import admin
from django.conf import settings
from datetime import datetime
from read.models import Read
from silo.models import Silo



class Country(models.Model):
    country = models.CharField("Country Name", max_length=255, blank=True)
    code = models.CharField("2 Letter Country Code", max_length=4, blank=True)
    description = models.CharField("Description/Notes", max_length=255, blank=True)
    latitude = models.CharField("Latitude", max_length=255, null=True, blank=True)
    longitude = models.CharField("Longitude", max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('country',)
        verbose_name_plural = "Countries"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Country, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.country


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Country'


class Program(models.Model):
    gaitid = models.CharField("GAITID", max_length=255, blank=True, unique=True)
    name = models.CharField("Program Name", max_length=255, blank=True)
    funding_status = models.CharField("Funding Status", max_length=255, blank=True)
    cost_center = models.CharField("Fund Code", max_length=255, blank=True, null=True)
    description = models.CharField("Program Description", max_length=765, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    country = models.ManyToManyField(Country)

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


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Program'


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


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date', 'edit_date')
    display = 'Province'


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


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'create_date', 'edit_date')
    display = 'District'


class Office(models.Model):
    name = models.CharField("Office Name", max_length=255, blank=True)
    code = models.CharField("Office Code", max_length=255, blank=True)
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
        super(Office, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'province', 'create_date', 'edit_date')
    display = 'Office'


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


class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date', 'edit_date')
    display = 'Village'


class Sector(models.Model):
    sector = models.CharField("Sector Name", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('sector',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Sector, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector', 'create_date', 'edit_date')
    display = 'Sector'


class Community(models.Model):
    name = models.CharField("Community", max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country)
    province = models.ForeignKey(Province, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True)
    village = models.ForeignKey(Village, null=True, blank=True)
    office = models.ForeignKey(Office, null=True, blank=True)
    latitude = models.CharField("Latitude (Coordinates)", max_length=255, blank=True, null=True)
    longitude = models.CharField("Longitude (Coordinates)", max_length=255, blank=True, null=True)
    community_rep = models.CharField("Community Representative", max_length=255, blank=True, null=True)
    community_rep_contact = models.CharField("Community Representative Contact", max_length=255, blank=True, null=True)
    community_mobilizer = models.CharField("Community Mobilizer", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Communities"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Community, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name','country','district','province','village','cluster', 'longitude','latitude','create_date', 'edit_date')
    display = 'Community'


class Contribution(models.Model):
    contributor = models.CharField("Contributor", max_length=255, blank=True)
    description = models.CharField("Description of Contribution", max_length=255, blank=True)
    value = models.CharField("Value of Contribution", max_length=255, blank=True)
    actual = models.BooleanField("Is an Actual Contribution", default=None)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('contributor',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Contribution, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.contributor


class ContributionAdmin(admin.ModelAdmin):
    list_display = ('contributor', 'create_date', 'edit_date')
    display = 'Contribution'


class QuantitativeOutputs(models.Model):
    number_achieved = models.CharField("Contributor", max_length=255, blank=True)
    description = models.CharField("Description of Contribution", max_length=255, blank=True)
    logframe_indicator = models.CharField("Logframe Indicator", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name_plural = "Quantitative Outputs"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(QuantitativeOutputs, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.description


class QuantitativeOutputsAdmin(admin.ModelAdmin):
    list_display = ('descrption', 'number_achieved', 'create_date', 'edit_date')
    display = 'Quantitative Outputs'


class Template(models.Model):
    name = models.CharField("Name of Document", max_length=135)
    documentation_type = models.CharField("Type (File or URL)", max_length=135)
    description = models.CharField(max_length=255)
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Template, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'documentation_type', 'file_field', 'create_date', 'edit_date')
    display = 'Template'


class ProjectProposal(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True, related_name="proposal")
    profile_code = models.CharField("Profile Code", max_length=255, blank=True, null=True)
    proposal_num = models.CharField("Proposal Number", max_length=255, blank=True, null=True)
    date_of_request = models.DateTimeField("Date of Request", null=True, blank=True)
    project_title = models.CharField("Project Title", max_length=255, blank=True, null=True)
    project_type = models.CharField("Project Type", max_length=255, blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True, null=True)
    prop_status = models.CharField("Proposal Status", max_length=255, blank=True, null=True)
    rej_letter = models.TextField("Rejection Letter", blank=True, null=True)
    activity_code = models.CharField("Activity Code", max_length=255, blank=True, null=True)
    project_description = models.TextField("Project Description", blank=True, null=True)
    approval = models.BooleanField("Approval", default=None)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="approving")
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="requesting")
    approval_remarks = models.CharField("Approval Remarks", max_length=255, blank=True, null=True)
    device_id = models.CharField("Device ID", max_length=255, blank=True, null=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    proposal_review = models.FileField("Proposal Review", upload_to='uploads', blank=True, null=True)
    proposal_review_2 = models.FileField("Proposal Review Additional", upload_to='uploads', blank=True, null=True)
    today = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    meta_instance_id = models.CharField("Meta Instance ID", max_length=255, blank=True, null=True)
    meta_instance_name = models.CharField("Meta Instance Name", max_length=255, blank=True, null=True)
    odk_id = models.CharField("ODK ID", max_length=255, blank=True, null=True)
    odk_uuid = models.CharField("ODK UUID", max_length=255, blank=True, null=True)
    odk_submission_time = models.DateTimeField("ODK Submission Time", null=True, blank=True)
    odk_index = models.CharField("ODK Index", max_length=255, blank=True, null=True)
    odk_parent_table_name = models.CharField("ODK Table Name", max_length=255, blank=True, null=True)
    odk_tags = models.CharField("ODK Tags", max_length=255, blank=True, null=True)
    odk_notes = models.CharField("ODK Notes", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)
    latitude = models.CharField("Latitude (Coordinates)", max_length=255, blank=True, null=True)
    longitude = models.CharField("Longitude (Coordinates)", max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('create_date',)
        permissions = (
             ("can_approve", "Can approve proposal"),
         )

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectProposal, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.project_title


class ProjectProposalAdmin(admin.ModelAdmin):
    list_display = ('project_title')
    display = 'project_title'


class ProjectAgreement(models.Model):
    project_proposal = models.ForeignKey(ProjectProposal, null=False, blank=False)
    program = models.ForeignKey(Program, null=True, blank=True, related_name="agreement")
    profile_code = models.CharField("Profile Code", max_length=255, blank=True, null=True)
    proposal_num = models.CharField("Proposal Number", max_length=255, blank=True, null=True)
    date_of_request = models.DateTimeField("Date of Request", blank=True, null=True)
    project_title = models.CharField("Project Title", max_length=255, blank=True, null=True)
    project_type = models.CharField("Proposal Number", max_length=255, blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True, null=True)
    prop_status = models.CharField("Proposal Status", max_length=255, blank=True, null=True)
    rej_letter = models.TextField("Rejection Letter", blank=True, null=True)
    activity_code = models.CharField("Activity Code", max_length=255, blank=True, null=True)
    office_code = models.CharField("Office Code", max_length=255, blank=True, null=True)
    cod_num = models.CharField("Project COD #", max_length=255, blank=True, null=True)
    sector = models.ForeignKey("Sector", blank=True, null=True)
    project_activity = models.CharField("Project Activity", max_length=255, blank=True, null=True)
    account_code = models.CharField("Account Code", max_length=255, blank=True, null=True)
    sub_code = models.CharField("Account Sub Code", max_length=255, blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True, null=True)
    staff_responsible = models.CharField("MC Staff Responsible", max_length=255, blank=True, null=True)
    partners = models.CharField("Partners", max_length=255, blank=True, null=True)
    name_of_partners = models.CharField("Name of Partners", max_length=255, blank=True, null=True)
    program_objectives = models.TextField("What Program Objectives does this help fulfill?", blank=True, null=True)
    mc_objectives = models.TextField("What MC strategic Objectives does this help fulfill?", blank=True, null=True)
    effect_or_impact = models.TextField("What is the anticipated effect of impact of this project?", blank=True, null=True)
    expected_start_date = models.DateTimeField(blank=True, null=True)
    expected_end_date = models.DateTimeField(blank=True, null=True)
    beneficiary_type = models.CharField("Type of direct beneficiaries", max_length=255, blank=True, null=True)
    num_direct_beneficiaries = models.CharField("Number of direct beneficiaries", max_length=255, blank=True, null=True)
    total_estimated_budget = models.CharField(max_length=255, blank=True, null=True)
    mc_estimated_budget = models.CharField(max_length=255, blank=True, null=True)
    other_budget = models.CharField(max_length=255, blank=True, null=True)
    estimation_date = models.DateTimeField(blank=True, null=True)
    estimated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="estimating")
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="checking")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="reviewing")
    approval = models.BooleanField("Approval", default=None)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="approving_agreement")
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="submitted_by_agreement")
    approval_remarks = models.CharField("Approval Remarks", max_length=255, blank=True, null=True)
    justification_background = models.TextField("General background and problem statement", blank=True, null=True)
    justification_description_community_selection = models.TextField("Description of community selection criteria", blank=True, null=True)
    description_of_project_activities = models.TextField(blank=True, null=True)
    description_of_government_involvement = models.TextField(blank=True, null=True)
    description_of_community_involvement = models.TextField(blank=True, null=True)
    documentation_government_approval = models.FileField("Upload Government Documentation of Approval", upload_to='uploads', blank=True, null=True)
    documentation_community_approval = models.FileField("Upload Community Documentation of Approval", upload_to='uploads', blank=True, null=True)
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)

    class Meta:
        ordering = ('create_date',)
        permissions = (
             ("can_approve", "Can approve proposal"),
         )

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectAgreement, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.project_title


class ProjectAgreementAdmin(admin.ModelAdmin):
    list_display = ('project_title')
    display = 'project_title'


class ProjectComplete(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True, related_name="complete")
    project_proposal = models.ForeignKey(ProjectProposal)
    project_agreement = models.ForeignKey(ProjectAgreement)
    project_title = models.CharField("Project Title", max_length=255, blank=True, null=True)
    activity_code = models.CharField("Activity Code", max_length=255, blank=True, null=True)
    project_name = models.CharField("Project Name", max_length=255, blank=True, null=True)
    expected_start_date = models.DateTimeField(blank=True, null=True)
    expected_end_date = models.DateTimeField(blank=True, null=True)
    actual_start_date = models.DateTimeField(blank=True, null=True)
    actual_end_date = models.DateTimeField(blank=True, null=True)
    on_time = models.BooleanField(default=None)
    no_explanation = models.TextField("If not on time explain delay", blank=True, null=True)
    estimated_budget = models.CharField("Estimated Budget", max_length=255, null=True, blank=True)
    actual_budget = models.CharField("Actual Budget", max_length=255, null=True, blank=True)
    budget_variance = models.CharField("Budget Variance", blank=True, null=True, max_length=255)
    explanation_of_variance = models.CharField("Explanation of variance", blank=True, null=True, max_length=255)
    actual_contribution = models.ForeignKey(Contribution)
    direct_beneficiaries = models.CharField("Actual Direct Beneficiaries", max_length=255, blank=True, null=True)
    jobs_created = models.CharField("Number of Jobs Created", max_length=255, blank=True, null=True)
    jobs_part_time = models.CharField("Part Time Jobs", max_length=255, blank=True, null=True)
    jobs_full_time = models.CharField("Full Time Jobs", max_length=255, blank=True, null=True)
    government_involvement = models.CharField("Government Involvement", max_length=255, blank=True, null=True)
    capacity_built = models.CharField("What capacity was built to ensure sustainability?", max_length=255, blank=True, null=True)
    issues_and_challenges = models.TextField("List any issues or challenges faced (include reasons for delays)", blank=True, null=True)
    lessons_learned= models.TextField("Lessons learned", blank=True, null=True)
    quantitative_outputs = models.ForeignKey(QuantitativeOutputs)
    community = models.ManyToManyField(Community, blank=True, null=True)
    estimated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="estimating_complete")
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="checking_complete")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="reviewing_complete")
    approval = models.BooleanField("Approval", default=None)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="approving_agreement_complete")
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="submitted_by_complete")
    approval_remarks = models.CharField("Approval Remarks", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)

    class Meta:
        ordering = ('create_date',)
        verbose_name_plural = "Project Completions"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectComplete, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.project_title


class ProjectCompleteAdmin(admin.ModelAdmin):
    list_display = ('program', 'project_name', 'activity_code')
    display = 'project_name'


class Documentation(models.Model):
    name = models.CharField("Name of Document", max_length=135)
    url = models.CharField("URL (Link to document or document repository)", blank=True, null=True, max_length=135)
    description = models.CharField(max_length=255)
    template = models.ForeignKey(Template, blank=True, null=True)
    silo = models.ForeignKey(Silo, blank=True, null=True)
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    project = models.ForeignKey(ProjectProposal, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

     #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Documentation, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Documentation"


class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'documentation_type', 'file_field', 'project_proposal_id', 'program_id', 'create_date', 'edit_date')
    display = 'Documentation'


class MergeMap(models.Model):
    read = models.ForeignKey(Read, null=False, blank=False)
    project_proposal = models.ForeignKey(ProjectProposal, null=True, blank=False)
    project_agreement = models.ForeignKey(ProjectAgreement, null=True, blank=False)
    project_completion = models.ForeignKey(ProjectComplete, null=True, blank=False)
    from_column = models.CharField(max_length=255, blank=True)
    to_column = models.CharField(max_length=255, blank=True)


class MergeMapAdmin(admin.ModelAdmin):
    list_display = ('read', 'project_proposal', 'project_agreement', 'project_completion', 'from_column', 'to_column')
    display = 'project_proposal'


class ProgramDashboard(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True)
    project_proposal = models.ForeignKey(ProjectProposal, null=True, blank=True)
    project_proposal_approved = models.IntegerField(null=True,blank=True)
    project_agreement = models.ForeignKey(ProjectAgreement, null=True, blank=True)
    project_agreement_approved = models.IntegerField(null=True,blank=True)
    project_completion = models.ForeignKey(ProjectComplete, null=True, blank=True)
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


class ProgramDashboardAdmin(admin.ModelAdmin):
    list_display = ('program', 'project_proposal', 'project_proposal_approved', 'create_date', 'edit_date')
    display = 'Program Dashboard'

