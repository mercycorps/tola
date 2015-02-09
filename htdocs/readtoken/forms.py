from django.forms import ModelForm
from read.models import Read
from .models import Token
from django.forms.models import inlineformset_factory


class ReadForm(ModelForm):
    class Meta:
        model = Read
        fields = '__all__'


TokenFormSet = inlineformset_factory(Read, Token, fields=('read_token', 'read_secret'), can_delete=False, extra=1)
EditTokenFormSet = inlineformset_factory(Read, Token, fields=('read_token', 'read_secret'), can_delete=False, extra=0)