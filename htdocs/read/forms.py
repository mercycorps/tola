from django.forms import ModelForm
from read.models import Read
import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Hidden
from crispy_forms.bootstrap import  FormActions


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
