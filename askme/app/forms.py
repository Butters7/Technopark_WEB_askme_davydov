from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList
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
        new_password = cleaned_data.get('new_password')
        new_password_check = cleaned_data.get('new_password_check')
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if username and models.User.objects.filter(username=username).exists():
            self.add_error('username', 'This username is already taken.')

        if new_password and new_password != new_password_check:
            self.add_error('new_password', '')
            self.add_error('new_password_check', "New password fields don't match.")

        if password and password != password_check:
            self.add_error('password', '')
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
            user.set_password(new_password)
            
        if username:
            profile.username = username
            user.username = username

        if email:
            user.email = email
            
        if avatar:
            profile.avatar = avatar

        user.save()
        profile.save()
        messages.success(request, 'Profile updated successfully!')
    

class RegistartionForm(forms.Form):
    username = forms.CharField(required=True, min_length=4)
    email = forms.EmailField(required=False, widget=forms.EmailInput)
    full_name = forms.CharField(required=False)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password_check = forms.CharField(required=True, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False, widget=forms.FileInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')
        full_name = cleaned_data.get('full_name')

        if email and models.User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already registred!')

        if username and models.User.objects.filter(username=username).exists():
            self.add_error('username', 'This username already exists!')

        if password and password != password_check:
            self.add_error('password', '')
            self.add_error('password_check', 'Password does not equal!')

        if full_name and len(full_name.split()) == 1:
            self.add_error('full_name', 'Full name must contain 2 words at least')

        return cleaned_data

    def save(self, request):
        user = models.User.objects.create_user(username=self.cleaned_data.get('username'))
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        profile = models.Profile.objects.create(profile=user)

        email = self.cleaned_data.get('email')
        full_name = self.cleaned_data.get('full_name')
        avatar = self.cleaned_data.get('avatar')

        if email:
            user.email = email

        if full_name:
            spliting_full_name = full_name.split()
            user.first_name = spliting_full_name[0]
            user.last_name = spliting_full_name[1::]

        if avatar:
            profile.avatar.save(avatar.name, avatar)

        user.save()
        profile.save()
        messages.success(request, 'Thanks for registration')


class AnswerForm(forms.Form):
    answer = forms.CharField(required=True, max_length=500, widget=forms.Textarea(attrs={'placeholder' : 'Enter an answer...'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].label = ''

    def save(self, request, question_id):
        user = models.User.objects.get(username=request.user)
        profile = models.Profile.objects.get(profile=user)
        question = models.Question.objects.get(id=question_id)
        answer = self.cleaned_data['answer']

        answer_obj = models.Answer.objects.create(text=answer, question=question, user_profile=profile)
        messages.success(request, 'Thanks for you answer!')

        return answer_obj


class AskForm(forms.Form):
    title = forms.CharField(required=True, max_length=50)
    description = forms.CharField(required=True, max_length=500, widget=forms.Textarea)
    tags = forms.CharField(required=True, max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        tags = cleaned_data.get('tags')

        if not title or not description or not tags:
            self.add_error(None, 'Please fill all fields!')

        tags_array = tags.split()
        for tag in tags_array:
            if len(tag) > 10:
                self.add_error('tags', f'Tag {tag} is too large (MaxLength of one tag is 10)!')
                break

        return cleaned_data
    
    def save(self, request):
        user = models.User.objects.get(username=request.user)
        profile = models.Profile.objects.get(profile=user)
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        tags_array = self.cleaned_data.get('tags').split()
        tags = []
        
        question = models.Question.objects.create(name=title, text=description, user_profile=profile)

        for tag in tags_array:
            tag_name, _ = models.Tag.objects.get_or_create(name=tag)
            tags.append(tag_name)

        question.tags.set(tags)
        question.save()

        return question
