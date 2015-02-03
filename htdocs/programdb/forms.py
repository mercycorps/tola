from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Field
from functools import partial
from widgets import GoogleMapsWidget
import floppyforms as forms
from django.forms.models import inlineformset_factory
from .models import ProjectProposal, ProgramDashboard, ProjectAgreement, Sector, Program

class ProgramDashboardForm(forms.ModelForm):

    class Meta:
        model = ProgramDashboard
        fields = '__all__'


class DatePicker(forms.DateInput):
    template_name = 'datepicker.html'

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class ProjectProposalForm(forms.ModelForm):

    class Meta:
        model = ProjectProposal
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    date_of_request = forms.DateInput()
    #hard coded 1 for country for now until configured in the form
    #TODO: configure country for each form
    program = forms.ModelChoiceField(queryset=Program.objects.filter(country='1', funding_status="Funded"))

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
            TabHolder(
                Tab('Details',
                    Fieldset('Program', 'program', 'profile_code', 'proposal_num', 'date_of_request', 'project_title', 'project_type',
                    ),
                    Fieldset(
                        'Community',
                        'community_rep','community_rep_contact','community_mobilizer'
                    ),
                ),
                Tab('Location',
                    Fieldset('Location',
                             'country', 'district', 'province', 'village', 'cluster'
                            ),
                    Fieldset('Map',
                     'map', 'latitude', 'longitude'
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
                             Field('approval', label="approved "), 'approved_by', 'approval_submitted_by',
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

class ProjectAgreementForm(forms.ModelForm):

    class Meta:
        model = ProjectAgreement
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    date_of_request = forms.DateInput()

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
            TabHolder(
                Tab('Executive Summary',
                    Fieldset('Program', 'program', 'project_proposal', 'profile_code', 'project_cod', 'sector', 'project_title', 'project_type',
                             'project_activity','account_code','sub_code','community','mc_staff_responsible'
                    ),
                    Fieldset(
                        'Partners',
                        'name_of_partners','program_objectives','mc_objectives','effect_or_impact','expected_Start_date',
                        'expected_end_date','beneficiary_type','num_beneficiaries','total_estimated_budget','mc_estimated_budget',
                        'estimation_date', 'estimated_by','checked_by','other_budget'
                    ),
                    Fieldset('Location',
                             'country', 'district', 'province', 'village', 'cluster'
                            ),
                    Fieldset('Map',
                     'map', 'latitude', 'longitude'
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
                        'documentation_government_approval',

                    ),
                ),

                Tab('Approval',
                    Fieldset('Approval',
                             Field('approval', label="approved "), 'approved_by', 'approval_submitted_by',
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

