from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Field
from functools import partial
from widgets import GoogleMapsWidget
import floppyforms as forms
from django.contrib.auth.models import Permission, User, Group
from .models import ProjectProposal, ProgramDashboard, ProjectAgreement, ProjectComplete, Sector, Program, Community, Documentation


class ProgramDashboardForm(forms.ModelForm):

    class Meta:
        model = ProgramDashboard
        fields = '__all__'


class DatePicker(forms.DateInput):
    """
    Use in form to create a Jquery datepicker element
    """
    template_name = 'datepicker.html'

    DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class ProjectProposalForm(forms.ModelForm):

    class Meta:
        model = ProjectProposal
        fields = '__all__'

    #hard coded 1 for country for now until configured in the form
    #TODO: configure country for each form
    program = forms.ModelChoiceField(queryset=Program.objects.filter(country='1', funding_status="Funded"))

    date_of_request = forms.DateField(widget=DatePicker.DateInput())

    def __init__(self,  *args, **kwargs):
        #get the user object to check permissions with
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Details',
                    Fieldset('Program', 'program', 'community_code', 'proposal_num', 'date_of_request', 'activity_code', 'project_title', 'project_type',
                    ),
                    Fieldset(
                        'Community',
                        'community', 'community_rep', 'community_rep_contact', 'community_mobilizer'
                    ),
                ),
                Tab('Description',
                    Fieldset(
                        'Proposal',
                        Field('project_description', rows="3", css_class='input-xlarge'),
                        Field('rej_letter', rows="3", css_class='input-xlarge'),
                        'project_code', 'prop_status', 'proposal_review', 'proposal_review_2',
                    ),
                ),
                Tab('Approval',
                    Fieldset('Approval',
                        PrependedText('approval', ''), 'approved_by', 'approval_submitted_by',
                        Field('approval_remarks', rows="3", css_class='input-xlarge')
                    ),
                ),
            ),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )


        super(ProjectProposalForm, self).__init__(*args, **kwargs)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            self.fields['approval'].widget.attrs['disabled'] = "disabled"
            self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_submitted_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"


class ProjectAgreementForm(forms.ModelForm):

    class Meta:
        model = ProjectAgreement
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput())
    expected_end_date = forms.DateField(widget=DatePicker.DateInput())
    estimation_date = forms.DateField(widget=DatePicker.DateInput())

    program = forms.ModelChoiceField(queryset=Program.objects.filter(country='1', funding_status="Funded"))

    documentation_government_approval = forms.FileField(required=False)
    documentation_community_approval = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):

        #get the user object from request to check permissions
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Executive Summary',
                    Fieldset('Program', 'program', 'project_proposal', 'activity_code', 'project_title', 'profile_code', 'project_cod', 'sector', 'project_type',
                             'project_activity','account_code','sub_code','community','mc_staff_responsible'
                    ),
                    Fieldset(
                        'Partners',
                        'name_of_partners','program_objectives','mc_objectives','effect_or_impact','expected_start_date',
                        'expected_end_date','beneficiary_type','num_beneficiaries','total_estimated_budget','mc_estimated_budget',
                        'estimation_date', 'estimated_by','checked_by','other_budget'
                    ),
                ),
                Tab('Justification and Description',
                    Fieldset(
                        'Justification',
                        Field('justification_background', rows="3", css_class='input-xlarge'),
                        Field('justification_description_community_selection', rows="3", css_class='input-xlarge'),
                    ),
                     Fieldset(
                        'Description',
                        Field('description_of_project_activities', rows="3", css_class='input-xlarge'),
                        Field('description_of_government_involvement', rows="3", css_class='input-xlarge'),
                        'documentation_government_approval',
                        Field('description_of_community_involvement', rows="3", css_class='input-xlarge'),
                        'documentation_community_approval',

                    ),
                ),
                Tab('Approval',
                    Fieldset('Approval',
                             PrependedText('approval', ''), 'approved_by', 'approval_submitted_by',
                             Field('approval_remarks', rows="3", css_class='input-xlarge')
                    ),
                ),
            ),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )
        super(ProjectAgreementForm, self).__init__(*args, **kwargs)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            self.fields['approval'].widget.attrs['disabled'] = "disabled"
            self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_submitted_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"

class ProjectCompleteForm(forms.ModelForm):

    class Meta:
        model = ProjectComplete
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput())
    expected_end_date = forms.DateField(widget=DatePicker.DateInput())
    actual_start_date = forms.DateField(widget=DatePicker.DateInput())
    actual_end_date = forms.DateField(widget=DatePicker.DateInput())

    program = forms.ModelChoiceField(queryset=Program.objects.filter(country='1', funding_status="Funded"))

    def __init__(self, *args, **kwargs):
        #get the user object from request to check permissions
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Executive Summary',
                    Fieldset('Program', 'program', 'project_proposal', 'project_agreement', 'activity_code', 'project_title'
                    ),
                    Fieldset(
                        'Dates',
                        'expected_start_date','expected_end_date', 'expected_duration', 'actual_start_date', 'actual_end_date', 'actual_duration',
                    ),
                ),
                Tab('Budget and Issues',
                    Fieldset(
                        'Budget',
                        'estimated_budget','actual_budget', 'budget_variance', 'explanation_of_variance', 'actual_contribution', 'direct_beneficiaries',
                        PrependedText('on_time', ''),'no_explanation',
                    ),
                     Fieldset(
                        'Jobs',
                        'jobs_created','jobs_part_time','jobs_full_time','government_involvement','capacity_built',

                    ),
                     Fieldset(
                        'Issues',
                        'issues_and_challenges','lessons_learned','quantitative_outputs'

                    ),
                ),

                Tab('Approval',
                    Fieldset('Approval',
                             PrependedText('approval', ''), 'approved_by', 'approval_submitted_by',
                             Field('approval_remarks', rows="3", css_class='input-xlarge')
                    ),
                ),
            ),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )
        super(ProjectCompleteForm, self).__init__(*args, **kwargs)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            self.fields['approval'].widget.attrs['disabled'] = "disabled"
            self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_submitted_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        exclude = ['create_date', 'edit_date']

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),

                'name','community_rep','community_rep_contact','community_mobilizer',
                'country','province','district','village','cluster', 'latitude','longitude',

            Fieldset(
                'Map',
                'map',

            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(CommunityForm, self).__init__(*args, **kwargs)


class DocumentationForm(forms.ModelForm):

    class Meta:
        model = Documentation
        exclude = ['create_date', 'edit_date']


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),

                'name', 'url', Field('description', rows="3", css_class='input-xlarge'), 'template', 'silo',
                'file_field','project',

            FormActions(
                Submit('submit', 'Submit', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(DocumentationForm, self).__init__(*args, **kwargs)
