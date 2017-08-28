from django.contrib.auth.models import User
from django import forms

from .models import Applicant

# Form to login and register a user
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']

# a modified form with additional profile pic to the django User
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('photo',)

# a form to update resume
class ResumeUpdate(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('resume',)

# a form to update profile details
class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )


class CvForm(forms.ModelForm):

    class Meta:
        model = Applicant
        fields = ['resume']