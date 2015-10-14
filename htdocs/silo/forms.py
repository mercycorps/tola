from django.core.urlresolvers import reverse_lazy
from django.forms import ModelForm
from silo.models import Silo, Read
#import floppyforms as forms
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field, Hidden
from crispy_forms.bootstrap import FormActions
from django.forms.formsets import formset_factory

class OnaLoginForm(forms.Form):
    username = forms.CharField(max_length=60, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('getOnaForms')
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Reset('rest', 'Reset', css_class='btn-warning'))
        super(OnaLoginForm, self).__init__(*args, **kwargs)
        

class SiloForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SiloForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # Append the read_id for edits and save button
        self.helper.layout.append(Submit('save', 'save'))
    class Meta:
        model = Silo
        fields = ['id', 'name', 'description', 'tags', 'shared', 'owner']


class NewColumnForm(forms.Form):

    new_column_name = forms.CharField(required=True, max_length=244)
    default_value = forms.CharField(required=False, max_length=244)
    silo_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-7'
        self.helper.html5_required = True
        self.helper.fields = ['silo_id', 'new_column_name', 'default_value']
        self.helper.add_input(Submit('save', 'save'))

        self.helper.layout = Layout(
            'silo_id',
            'new_column_name',
            'default_value',
        )
        super(NewColumnForm, self).__init__(*args, **kwargs)


#READ FORMS
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
        fields = ['read_name', 'read_url', 'description','type','file_data', 'owner']
        #exclude = ['create_date',]

class UploadForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout.append(Field('file_data'))
        # Append the read_id for edits and save button
        self.helper.layout.append(Hidden('read_id', '{{read_id}}'))
        self.helper.form_tag = False


class FileField(Field):
    template_name = 'filefield.html'


class EditColumnForm(forms.Form):
    """
    A form that saves a document from mongodb
    """
    id = forms.CharField(required=False, max_length=24, widget=forms.HiddenInput())
    silo_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop("extra")
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-5'
        self.helper.field_class = 'col-sm-7'
        #self.helper.label_size = ' col-sm-offset-2'
        self.helper.html5_required = True
        self.helper.form_tag = True
        self.helper.add_input(Submit('save', 'save'))
        super(EditColumnForm, self).__init__(*args, **kwargs)

        for item in extra:
            print item
            if item != "_id" and item != "silo_id" and item != "edit_date" and item != "create_date":
                self.fields[item] = forms.CharField(label=item, initial=item, required=False,widget="")
                self.fields[item + "_delete"] = forms.BooleanField(label="delete " + item, initial=False, required=False,widget="")

class MongoEditForm(forms.Form):
    """
    A form that saves a document from mongodb
    """
    id = forms.CharField(required=False, max_length=24, widget=forms.HiddenInput())
    silo_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop("extra")
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-5'
        self.helper.field_class = 'col-sm-7'
        self.helper.html5_required = True
        self.helper.form_tag = False
        super(MongoEditForm, self).__init__(*args, **kwargs)

        for item in extra:
            if item == "edit_date" or item == "create_date":
                self.fields[item] = forms.CharField(label = item, initial=extra[item], required=False, widget=forms.TextInput(attrs={'readonly': "readonly"}))
            elif item != "_id" and item != "silo_id":
                self.fields[item] = forms.CharField(label = item, initial=extra[item], required=False)


