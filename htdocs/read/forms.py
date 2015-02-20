from django.forms import ModelForm
from read.models import Read
import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Hidden, Fieldset
from crispy_forms.bootstrap import FormActions
from django.forms.formsets import formset_factory


class ReadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReadForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # Append the read_id for edits and save button
        self.helper.layout.append(Hidden('read_id', '{{read_id}}'))
        self.helper.layout.append(Submit('save', 'save'))


    class Meta:
        model = Read
        fields = ['read_name', 'read_url', 'description','type','file_data','owner']


class ODKForm(forms.Form):

    choices = (
        ('', '-- Select --'),
        ('https://ona.io/api/v1/data', 'Ona'),
        ('https://formhub.org/api/v1/data', 'Formhub')
    )
    source = forms.ChoiceField(choices, required=False)
    url_source = forms.Field(required=False)


    def __init__(self, *args, **kwargs):
        super(ODKForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # Append the read_id for edits and save button
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
                'Choose a Source',
                'source'
            ),
            Fieldset(
                'OR - Enter URL to local or hosted ODK Collect',
                'url_source'
            ),
            FormActions(
                Submit('submit', 'Next >>', css_class='btn-default'),
            ),

        )


class UploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # Append the read_id for edits and save button
        self.helper.layout.append(Hidden('read_id', '{{read_id}}'))
        self.helper.form_tag = False

class FileField(Field):
    template_name = 'filefield.html'
