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
        return self.sector


class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector', 'create_date', 'edit_date')
    display = 'Sector'


class Community(models.Model):
    name = models.CharField("Community", max_length=255, blank=True, null=True)
    code = models.CharField("Code Name", max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country)
    province = models.ForeignKey(Province, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True)
    village = models.ForeignKey(Village, null=True, blank=True)
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
        self.code = str(self.country.code) + "-" + str(self.office.code) + "-" + str(self.name)
        super(Community, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country', 'district', 'province', 'village', 'cluster', 'longitude', 'latitude', 'create_date', 'edit_date')
    display = 'Community'


class Capacity(models.Model):
    capacity = models.CharField("Capacity", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('capacity',)
        verbose_name_plural = "Capacity"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Capacity, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.capacity


class CapacityAdmin(admin.ModelAdmin):
    list_display = ('capacity', 'create_date', 'edit_date')
    display = 'Capacity'


class Evaluate(models.Model):
    evaluate = models.CharField("How will you evaluate the outcome or impact of the project?", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('evaluate',)
        verbose_name_plural = "Evaluate"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Evaluate, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.capacity


class EvaluateAdmin(admin.ModelAdmin):
    list_display = ('evaluate', 'create_date', 'edit_date')
    display = 'Evaluate'


class ProjectType(models.Model):
    name = models.CharField("Type of Project", max_length=135)
    description = models.CharField(max_length=255)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectType, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Project Type'


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

class Budget(models.Model):
    contributor = models.CharField(max_length=135)
    description_of_contribution = models.CharField(max_length=255)
    proposed_value = models.CharField(max_length="255", blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Template, self).save()

    def __unicode__(self):
        return self.contributor

    class Meta:
        ordering = ('contributor',)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('contributor', 'description_of_contribution', 'proposed_value', 'create_date', 'edit_date')
    display = 'Budget'


class ProjectProposal(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True, related_name="proposal")
    proposal_num = models.CharField("Proposal Number", max_length=255, blank=True, null=True)
    date_of_request = models.DateTimeField("Date of Request", null=True, blank=True)
    project_name = models.CharField("Project Name", help_text='Please be specific in your name.  Consider that your Project Name includes WHO, WHAT, WHERE, HOW', max_length=255)
    sector = models.ForeignKey(Sector, max_length=255, blank=True, null=True)
    project_type = models.ForeignKey(ProjectType, help_text='Please refer to Form 05 - Project Progress Summary', max_length=255, blank=True, null=True)
    project_activity = models.CharField("Project Activity", help_text='This should come directly from the activities listed in the Logframe', max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, null=True, blank=True)
    community = models.ManyToManyField(Community, blank=True, null=True)
    community_rep = models.CharField("Community Representative", max_length=255, blank=True, null=True)
    community_rep_contact = models.CharField("Community Representative Contact", help_text='Can have mulitple contact numbers', max_length=255, blank=True, null=True)
    community_mobilizer = models.CharField("MC Community Mobilizer", max_length=255, blank=True, null=True)
    community_mobilizer_contact = models.CharField("MC Community Mobilizer Contact Number", max_length=255, blank=True, null=True)
    has_rej_letter = models.BooleanField("If Rejected: Rejection Letter Sent?", help_text='If yes attach copy', default=False)
    rejection_letter = models.FileField("Rejection Letter", upload_to='uploads', blank=True, null=True)
    activity_code = models.CharField("Activity Code", help_text='If applicable at this stage, please request Activity Code from Kabul MEL', max_length=255, blank=True, null=True)
    project_description = models.TextField("Project Description", help_text='Description must meet the Criteria.  Will translate description into three languages: English, Dari and Pashto)', blank=True, null=True)
    approval = models.CharField("Approval", default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,help_text='This is the Provincial Line Manager', blank=True, null=True, related_name="approving")
    estimated_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='This is the originator', blank=True, null=True, related_name="estimate")
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="requesting")
    approval_remarks = models.CharField("Approval Remarks", max_length=255, blank=True, null=True)
    device_id = models.CharField("Device ID", max_length=255, blank=True, null=True)
    date_approved = models.DateTimeField(null=True, blank=True)
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
        return self.project_name


class ProjectProposalAdmin(admin.ModelAdmin):
    list_display = ('project_name')
    display = 'project_name'


class ProjectAgreement(models.Model):
    project_proposal = models.ForeignKey(ProjectProposal, null=False, blank=False)
    program = models.ForeignKey(Program, null=True, blank=True, related_name="agreement")
    date_of_request = models.DateTimeField("Date of Request", blank=True, null=True)
    project_name = models.CharField("Project Name", help_text='Please be specific in your name.  Consider that your Project Name includes WHO, WHAT, WHERE, HOW', max_length=255, blank=True, null=True)
    project_type = models.CharField("Project Type", help_text='Please refer to Form 05 - Project Progress Summary', max_length=255, blank=True, null=True)
    project_activity = models.CharField("Project Activity", help_text='This should come directly from the activities listed in the Logframe', max_length=255, blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True, null=True)
    activity_code = models.CharField("Activity Code", help_text='Please request Activity Code from Kabul MEL', max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, null=True, blank=True)
    cod_num = models.CharField("Project COD #", max_length=255, blank=True, null=True)
    sector = models.ForeignKey("Sector", blank=True, null=True)
    external_stakeholder_list = models.FileField("External stakeholder list", help_text="Please refer to PM@MC Section 01: Identification and Design under 1.1", upload_to='uploads', blank=True, null=True)
    project_activity = models.CharField("Project Activity", max_length=255, blank=True, null=True)
    project_design = models.CharField("Project design for", max_length=255, blank=True, null=True)
    account_code = models.CharField("Account Code", help_text='optional - request from finance', max_length=255, blank=True, null=True)
    lin_code = models.CharField("LIN Sub Code", help_text='optional - request from finance', max_length=255, blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True, null=True)
    staff_responsible = models.CharField("MC Staff Responsible", max_length=255, blank=True, null=True)
    partners = models.BooleanField("Are there partners involved?", default=0)
    name_of_partners = models.CharField("Name of Partners", max_length=255, blank=True, null=True)
    program_objectives = models.TextField("What Program Objectives does this help fulfill?", blank=True, null=True)
    mc_objectives = models.TextField("What MC strategic Objectives does this help fulfill?", blank=True, null=True)
    effect_or_impact = models.TextField("What is the anticipated effect of impact of this project?", blank=True, null=True)
    expected_start_date = models.DateTimeField("Expected starting date", blank=True, null=True)
    expected_end_date = models.DateTimeField("Expected ending date",blank=True, null=True)
    expected_duration = models.CharField("Expected duration", help_text="[MONTHS]/[DAYS]", blank=True, null=True, max_length=255)
    beneficiary_type = models.CharField("Type of direct beneficiaries", help_text="i.e. Farmer, Association, Student, Govt, etc.", max_length=255, blank=True, null=True)
    estimated_num_direct_beneficiaries = models.CharField("Estimated number of direct beneficiaries", help_text="Please provide achievable estimates as we will use these as are 'Targets'",max_length=255, blank=True, null=True)
    average_household_size = models.CharField("Average Household Size", help_text="Refer to Form 01 - Community Profile",max_length=255, blank=True, null=True)
    estimated_num_indirect_beneficiaries = models.CharField("Estimated Number of indirect beneficiaries", help_text="This is a calculation - multiply direct beneficiaries by average household size",max_length=255, blank=True, null=True)
    total_estimated_budget = models.CharField(help_text="In USD", max_length=255, blank=True, null=True)
    mc_estimated_budget = models.CharField(help_text="In USD", max_length=255, blank=True, null=True)
    other_budget = models.ForeignKey(Budget, help_text="Describe and quantify in dollars", blank=True, null=True)
    estimation_date = models.DateTimeField(blank=True, null=True)
    estimated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="estimating")
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="checking")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="reviewing")
    capacity = models.ForeignKey(Capacity, blank=True, null=True, related_name="quant_out_agree")
    evaluate = models.ForeignKey(Evaluate, blank=True, null=True, related_name="quant_out_agree")
    approval = models.CharField("Approval", default="in progress", max_length=255, blank=True, null=True)
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
        return self.project_name


class ProjectAgreementAdmin(admin.ModelAdmin):
    list_display = ('project_name')
    display = 'project_name'


class ProjectComplete(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True, related_name="complete")
    project_proposal = models.ForeignKey(ProjectProposal)
    project_agreement = models.ForeignKey(ProjectAgreement)
    activity_code = models.CharField("Activity Code", max_length=255, blank=True, null=True)
    project_name = models.CharField("Project Name", max_length=255, blank=True, null=True)
    project_activity = models.CharField("Project Activity", max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, null=True, blank=True)
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
    direct_beneficiaries = models.CharField("Actual Direct Beneficiaries", max_length=255, blank=True, null=True)
    jobs_created = models.CharField("Number of Jobs Created", max_length=255, blank=True, null=True)
    jobs_part_time = models.CharField("Part Time Jobs", max_length=255, blank=True, null=True)
    jobs_full_time = models.CharField("Full Time Jobs", max_length=255, blank=True, null=True)
    government_involvement = models.CharField("Government Involvement", max_length=255, blank=True, null=True)
    capacity_built = models.CharField("What capacity was built to ensure sustainability?", max_length=255, blank=True, null=True)
    issues_and_challenges = models.TextField("List any issues or challenges faced (include reasons for delays)", blank=True, null=True)
    lessons_learned= models.TextField("Lessons learned", blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True, null=True)
    estimated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="estimating_complete")
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="checking_complete")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="reviewing_complete")
    approval = models.CharField("Approval", default="in progress", max_length=255, blank=True, null=True)
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


class Benchmarks(models.Model):
    percent_complete = models.IntegerField("% complete", max_length=25, blank=True, null=True)
    percent_cumulative = models.IntegerField("% cumulative completion", max_length=25, blank=True, null=True)
    description = models.CharField("Description", max_length=255, blank=True)
    agreement = models.ForeignKey(ProjectAgreement,blank=True, null=True)
    complete = models.ForeignKey(ProjectComplete,blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name_plural = "Benchmarks"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Benchmarks, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.description


class BenchmarksAdmin(admin.ModelAdmin):
    list_display = ('description', 'percent_complete', 'percent_cumulative', 'create_date', 'edit_date')
    display = 'Benchmarks'


class Monitor(models.Model):
    responsible_person = models.CharField("Person Responsible", max_length=25, blank=True, null=True)
    frequency = models.IntegerField("Frequency", max_length=25, blank=True, null=True)
    type = models.TextField("Type", null=True, blank=True)
    agreement = models.ForeignKey(ProjectAgreement,blank=True, null=True)
    complete = models.ForeignKey(ProjectComplete,blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('type',)
        verbose_name_plural = "Monitors"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Monitor, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.description


class MonitorAdmin(admin.ModelAdmin):
    list_display = ('responsible_person', 'frequency', 'type', 'create_date', 'edit_date')
    display = 'Monitor'


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

class TrainingAttendance(models.Model):
    training_name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, null=True, blank=True)
    project_proposal = models.ForeignKey(ProjectProposal, null=True, blank=True)
    implementer = models.CharField(max_length=255, null=True, blank=True)
    reporting_period = models.CharField(max_length=255, null=True, blank=True)
    total_participants = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    community = models.CharField(max_length=255, null=True, blank=True)
    training_duration = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    trainer_name = models.CharField(max_length=255, null=True, blank=True)
    trainer_contact_num = models.CharField(max_length=255, null=True, blank=True)
    form_filled_by = models.CharField(max_length=255, null=True, blank=True)
    form_filled_by_contact_num = models.CharField(max_length=255, null=True, blank=True)
    total_male = models.IntegerField(null=True, blank=True)
    total_female = models.IntegerField(null=True, blank=True)
    total_age_0_14_male = models.IntegerField(null=True, blank=True)
    total_age_0_14_female = models.IntegerField(null=True, blank=True)
    total_age_15_24_male = models.IntegerField(null=True, blank=True)
    total_age_15_24_female = models.IntegerField(null=True, blank=True)
    total_age_25_59_male = models.IntegerField(null=True, blank=True)
    total_age_25_59_female = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('training_name',)

    #onsave add create date or update edit date
    def save(self):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(TrainingAttendance, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return unicode(self.training_name)


class TrainingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('training_name', 'program', 'project_proposal', 'create_date', 'edit_date')
    display = 'Program Dashboard'

class Beneficiary(models.Model):
    beneficiary_name = models.CharField(max_length=255, null=True, blank=True)
    training = models.ForeignKey(TrainingAttendance, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    community = models.ForeignKey(Community, null=True, blank=True)
    signature = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('beneficiary_name',)

    #onsave add create date or update edit date
    def save(self):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Beneficiary, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return unicode(self.program)


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('beneficiary_name', 'father_name', 'age', 'gender', 'community', 'signature', 'remarks', 'initials')

class Contribution(models.Model):
    contributor = models.CharField("Contributor", max_length=255, blank=True)
    description = models.CharField("Description of Contribution", max_length=255, blank=True)
    value = models.CharField("Value of Contribution", max_length=255, blank=True)
    actual = models.BooleanField("Is an Actual Contribution", default=None)
    project_agreement = models.ForeignKey(ProjectAgreement, blank=True, null=True, related_name="c_agreement")
    project_complete = models.ForeignKey(ProjectComplete, blank=True, null=True, related_name="c_complete")
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
    targeted = models.CharField("Targeted #", max_length=255, blank=True, null=True)
    description = models.CharField("Description of Contribution", max_length=255, blank=True, null=True)
    logframe_indicator = models.ForeignKey('indicators.Indicator', blank=True, null=True)
    non_logframe_indicator = models.CharField("Logframe Indicator", max_length=255, blank=True, null=True)
    project_agreement = models.ForeignKey(ProjectAgreement, blank=True, null=True, related_name="q_agreement")
    project_complete = models.ForeignKey(ProjectAgreement, blank=True, null=True, related_name="q_complete")
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
    list_display = ('description', 'targeted', 'logframe_indicator', 'create_date', 'edit_date')
    display = 'Quantitative Outputs'

