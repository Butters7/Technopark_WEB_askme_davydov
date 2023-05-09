from django import forms
from app import models
from django.contrib import messages


def checkAuth(request) :
    if request.user.is_authenticated:
        user = models.User.objects.get(username=request.user)
        return models.Profile.objects.get(profile=user)
    else:
        return None


class LoginForm(forms.Form) :
    username = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


class SettingForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False, widget=forms.EmailInput)
    password = forms.CharField(required=True, min_length=8, widget=forms.PasswordInput)
    password_check = forms.CharField(required=True, min_length=8, widget=forms.PasswordInput)
    new_password = forms.CharField(required=False, min_length=8, widget=forms.PasswordInput)
    new_password_check = forms.CharField(required=False, min_length=8, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False, widget=forms.FileInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        new_password = cleaned_data.get('new_password')
        new_password_check = cleaned_data.get('new_password_check')
        avatar = cleaned_data.get('avatar')
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')
        changed_fields = []
        changed_fields.append('password')

        if username:
            if models.User.objects.filter(username=username).exists():
                self.add_error('username', 'This username is already taken.')
            else:
                changed_fields.append('username')

        if email:
            changed_fields.append('email')

        if new_password:
            changed_fields.extend(['new_password', 'new_password_check'])

        if avatar:
            changed_fields.append('avatar')

        if 'new_password' in changed_fields and new_password != new_password_check:
            self.add_error('new_password_check', "New password fields don't match.")
        if 'password' in changed_fields and password != password_check:
            self.add_error('password_check', "Password fields don't match.")

        return cleaned_data
    
    def save(self, request):
        user = models.User.objects.get(username=request.user)
        profile = models.Profile.objects.get(profile=user)
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        new_password = self.cleaned_data.get('new_password')
        avatar = self.cleaned_data.get('avatar')

        if new_password:
            user.set_password(self.cleaned_data['new_password'])
            
        if username:
            profile.username = self.cleaned_data['username']
            user.username = self.cleaned_data['username']

        if email:
            user.email = self.cleaned_data['email']
            
        if avatar:
            profile.avatar = self.cleaned_data['avatar']

        user.save()
        profile.save()
        messages.success(request, 'Profile updated successfully!')
    