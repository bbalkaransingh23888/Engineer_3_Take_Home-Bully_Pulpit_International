from django import forms
from .models import Audience

class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ['file']

