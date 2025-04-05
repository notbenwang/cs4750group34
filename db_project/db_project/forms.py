from django import forms
from db_project.models import Appuser

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Appuser
        fields = ['biography']