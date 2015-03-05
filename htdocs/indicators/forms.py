from django.forms import ModelForm
from indicators.models import Indicator
from activitydb.models import Program
import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Hidden, Fieldset
from crispy_forms.bootstrap import FormActions


class IndicatorForm(forms.ModelForm):

    class Meta:
        model = Indicator
        fields = ['indicator_type', 'name', 'description', 'sector', 'owner', 'program']

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
            Fieldset(
                    'indicator_type','name', 'description','sector','owner','program'
                ),
            )

        super(IndicatorForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # Append the read_id for edits and save button
        self.helper.layout.append(Submit('save', 'save'))
