from django import forms
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)


class GroupForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=True)
    group_type = forms.ChoiceField(choices=[('public', 'Public'), ('private', 'Private')],
                                   widget=forms.Select(attrs={'class': 'form-control'}))


class PostForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=True)


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=True)
    parent_comment_id = forms.IntegerField(required=False, widget=forms.HiddenInput())


class EditBioForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)


class StepDownForm(forms.Form):
    new_admin_id = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        moderators = kwargs.pop('moderators', [])
        super().__init__(*args, **kwargs)
        self.fields['new_admin_id'].choices = [(mod['user_id'], mod['username']) for mod in moderators]


class AppointModeratorForm(forms.Form):
    user_id = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        members = kwargs.pop('members', [])
        super().__init__(*args, **kwargs)
        self.fields['user_id'].choices = [(member['user_id'], member['username']) for member in members]


class ApproveJoinForm(forms.Form):
    request_id = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        requests = kwargs.pop('requests', [])
        super().__init__(*args, **kwargs)
        self.fields['request_id'].choices = [(req['request_id'], req['username']) for req in requests]


class BanUserForm(forms.Form):
    user_id = forms.CharField(widget=forms.HiddenInput())
    reason = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class UnbanUserForm(forms.Form):
    user_id = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        banned_users = kwargs.pop('banned_users', [])
        super().__init__(*args, **kwargs)
        self.fields['user_id'].choices = [(user['user_id'], user['username']) for user in banned_users]