from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Textarea, TextInput, Select, SelectMultiple, FileInput,EmailInput
from .models import CustomUser
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phoneNumber = forms.CharField(required=True)
    profilePicture = forms.ImageField(required=False)
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ("email", "phoneNumber", "username", "first_name", "last_name", "profilePicture", "password1", "password2")
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phoneNumber = self.cleaned_data["phoneNumber"]
        user.profilePicture = self.cleaned_data["profilePicture"]
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control '}), required=True)
    phoneNumber = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),  required=True)
    profilePicture = forms.ImageField( required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phoneNumber",  "first_name", "last_name", "profilePicture")
