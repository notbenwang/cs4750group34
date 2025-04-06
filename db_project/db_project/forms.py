from django import forms
from db_project.models import Appuser, Community

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Appuser
        fields = ['biography']

class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'about']