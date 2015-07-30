from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset
#import floppyforms as forms
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


from .models import Feedback


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'


    severity = forms.ChoiceField(
        label="Priority",
        choices=(("High", "High"), ("Medium", "Medium"), ("Low", "Low")),
        widget=forms.Select,
        initial='2',
        required=True,
    )

    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-6'
    helper.form_error_title = 'Form Errors'
    helper.error_text_inline = True
    helper.help_text_inline = True
    helper.html5_required = True
    helper.layout = Layout(Fieldset('', 'submitter', 'note', 'page', 'severity'),Submit('submit', 'Submit', css_class='btn-default'), Reset('reset', 'Reset', css_class='btn-warning'))

"""
Form for registering a new account.
"""


class RegistrationForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = '__all__'

    email = forms.EmailField(widget=forms.TextInput, label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)")
    username = forms.CharField(widget=forms.TextInput, label="User Name")
    first_name = forms.CharField(widget=forms.TextInput, label="First Name")
    last_name = forms.CharField(widget=forms.TextInput, label="Last Name")

    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-6'
    helper.form_error_title = 'Form Errors'
    helper.error_text_inline = True
    helper.help_text_inline = True
    helper.html5_required = True
    helper.layout = Layout(Fieldset('', 'email', 'username', 'first_name', 'last_name', 'password1', 'password2'), Submit('submit', 'Submit', css_class='btn-default'), Reset('reset', 'Reset', css_class='btn-warning'))



