from django.forms import ModelForm
from indicators.models import Program, Indicator
import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Hidden
from crispy_forms.bootstrap import  FormActions


class ProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgramForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # Append the read_id for edits and save button
        self.helper.layout.append(Submit('save', 'save'))
    class Meta:
        model = Program
        fields = ['grantid','name','sector', 'storagebin_url', 'description','sector','owner']


class IndicatorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IndicatorForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # Append the read_id for edits and save button
        self.helper.layout.append(Submit('save', 'save'))
    class Meta:
        model = Indicator
        fields = ['indicator_type','name', 'description', 'activity','period','sector','target','target_actual','disaggregation_type','budget','budget_actual','owner','program']


class ProgramIndicatorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgramIndicatorForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # Append the read_id for edits and save button
        self.helper.layout.append(Submit('save', 'save'))
    class Meta:
        model = Indicator
        fields = ['indicator_type','name', 'description', 'activity','period','sector','target','target_actual','disaggregation_type','budget','budget_actual','owner','program']