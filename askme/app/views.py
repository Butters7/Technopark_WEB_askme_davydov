from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from app import models
from app import forms


@login_required(login_url='/login')
def ask(request):
    account = forms.checkAuth(request=request)
    context = models.get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['account'] = account

    return render(request, 'ask.html', context)


def base(request):
    account = forms.checkAuth(request=request)
    context = models.get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['account'] = account

    return render(request, 'base.html', context)


def index(request):
    account = forms.checkAuth(request=request)
    page_obj = models.createPaginator(models.Question.objects.get_news_question(), request)
    context = models.get_context(page_obj, models.Tag.objects.get_popular_tags(), models.Profile.objects.get_five_best_members())
    context['account'] = account

    return render(request, 'index.html', context)


def log_in(request):

    if request.method == 'GET':
        login_form = forms.LoginForm()
    elif request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")
            
    context = { 'tags' : models.Tag.objects.get_popular_tags(), 'best_members' : models.Profile.objects.get_five_best_members(), 'form' : login_form }

    return render(request, 'login.html', context)


@login_required(login_url='/login')
def settings(request):
    account = forms.checkAuth(request=request)

    if request.method == 'GET':
        setting_form = forms.SettingForm()
    elif request.method == 'POST':
        setting_form = forms.SettingForm(request.POST)
        if setting_form.is_valid():
            password = setting_form.cleaned_data.get('password')
            if not account.profile.check_password(password):
                setting_form.add_error(None, 'Current password are not equal')
            else:
                setting_form.save(request)
                return redirect(reverse('settings'))

    context = { 'tags' : models.Tag.objects.get_popular_tags(), 'best_members' : models.Profile.objects.get_five_best_members(), 'form' : setting_form, 'account' : account }

    return render(request, 'settings.html', context)


def question(request, question_id):
    if not models.Question.objects.filter(pk=question_id):
        raise Http404(f'Question_id {question_id} does not exist')
    
    account = forms.checkAuth(request=request)
    page_obj = models.createPaginator(models.Question.objects.get_popular_answers(question_id), request)
    context = models.get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['question'] = models.Question.objects.get(pk=question_id)
    context['account'] = account

    return render(request, 'question.html', context)


def signup(request):
    context = models.get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'signup.html', context)


def tag(request, tag_name):
    if not models.Tag.objects.filter(name=tag_name):
        raise Http404(f'Tag {tag_name} does not exist')

    account = forms.checkAuth(request=request)
    page_obj = models.createPaginator(models.Question.objects.get_question_with_special_tag(tag_name), request)
    context = models.get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['tag_name'] = tag_name
    context['account'] = account

    return render(request, 'tag.html', context)


def hot(request):
    account = forms.checkAuth(request=request)
    page_obj = models.createPaginator(models.Question.objects.get_hot_questions(), request)
    context = models.get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['account'] = account

    return render(request, 'hot.html', context)


def log_out(request):
    auth.logout(request)

    return redirect('index')
