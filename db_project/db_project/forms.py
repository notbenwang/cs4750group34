from django import forms
from .models import Appuser, Community, Comment, Posts
import re

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Appuser
        fields = ['biography']

class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'about']

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Add a comment…"}
            )
        }
        labels = {"content": ""}


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4})
        }
        labels = {"content": "Edit your comment"}

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content']