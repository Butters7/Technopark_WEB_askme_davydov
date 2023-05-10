from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
from app import models
from app import forms


@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def ask(request):
    account = forms.checkAuth(request=request)

    if request.method == 'GET':
        ask_form = forms.AskForm()
    elif request.method == 'POST':
        ask_form = forms.AskForm(request.POST)
        if ask_form.is_valid():
            question = ask_form.save(request)
            return redirect(reverse('question', args=[question.id]))
        
    context = { 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(), 
        'form' : ask_form, 
        'account' : account, 
        'path' : request.path 
    }

    return render(request, 'ask.html', context)


@require_http_methods(['GET'])
def base(request):
    account = forms.checkAuth(request=request)

    context = { 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(),
        'account' : account,
        'path' : request.path,
    }

    return render(request, 'base.html', context)


@require_http_methods(['GET'])
def index(request):
    account = forms.checkAuth(request=request)
    page_obj = models.createPaginator(models.Question.objects.get_news_question(), request)

    context = { 
        'page_obj' : page_obj, 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(),
        'account' : account,
        'path' : request.path,
    }

    return render(request, 'index.html', context)


@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'GET':
        login_form = forms.LoginForm()
    elif request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                messages.success(request, 'You are in!')
                reverse_url = request.GET.get('next')
                return redirect(reverse_url if reverse_url else reverse('index'))
            login_form.add_error(None, "Invalid username or password")
            
    context = { 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(), 
        'form' : login_form,
    }

    return render(request, 'login.html', context)


@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def settings(request):
    account = forms.checkAuth(request=request)

    if request.method == 'GET':
        setting_form = forms.SettingForm()
    elif request.method == 'POST':
        setting_form = forms.SettingForm(request.POST, files=request.FILES)
        if setting_form.is_valid():
            password = setting_form.cleaned_data.get('password')
            if not account.profile.check_password(password):
                setting_form.add_error(None, 'Current password are not equal')
            else:
                setting_form.save(request)
                return redirect(reverse('settings'))

    context = { 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(), 
        'form' : setting_form, 
        'account' : account, 
        'path' : request.path 
    }

    return render(request, 'settings.html', context)


@require_http_methods(['GET', 'POST'])
def question(request, question_id):
    if not models.Question.objects.filter(pk=question_id):
        raise Http404(f'Question_id {question_id} does not exist')
    
    account = forms.checkAuth(request=request)

    context = { 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(), 
        'question' : models.Question.objects.get(pk=question_id), 
        'account' : account,  
        'path' : request.path 
    }
    
    if request.method == 'GET':
        page_obj = models.createPaginator(models.Question.objects.get_popular_answers(question_id), request)
        context['page_obj'] = page_obj
        answer_form = forms.AnswerForm()
    elif request.method == 'POST':
        if not account:
            return redirect(reverse('login'))
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(request, question_id)
            context['form'] = forms.AnswerForm()
            list_obj = models.Question.objects.get_popular_answers(question_id)
            paginator = models.Paginator(list_obj, 3)

            for page_number in paginator.page_range:
                page_obj = paginator.get_page(page_number)

                for obj in page_obj.object_list:
                    if obj.id == answer.id:
                        return redirect(reverse('question', args=[question_id]) + f'?page={page_obj.number}')
        
    context['form'] = answer_form

    return render(request, 'question.html', context)


@require_http_methods(['GET', 'POST'])
def signup(request):
    account = forms.checkAuth(request=request)
    if account:
        redirect(reverse('index'))

    if request.method == 'GET':
        registration_form = forms.RegistartionForm()
    elif request.method == 'POST':
        registration_form = forms.RegistartionForm(request.POST, files=request.FILES)
        if registration_form.is_valid():
            registration_form.save(request)
            username = registration_form.cleaned_data.get('username')
            password = registration_form.cleaned_data.get('password')
            user_auth = auth.authenticate(username=username, password=password)
            auth.login(request, user_auth)
            return redirect(reverse('index'))

    context = { 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(), 
        'form' : registration_form 
    }

    return render(request, 'signup.html', context)


@require_http_methods(['GET'])
def tag(request, tag_name):
    if not models.Tag.objects.filter(name=tag_name):
        raise Http404(f'Tag {tag_name} does not exist')

    account = forms.checkAuth(request=request)
    page_obj = models.createPaginator(models.Question.objects.get_question_with_special_tag(tag_name), request)

    context = { 
        'page_obj' : page_obj, 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(),
        'tag_name' : tag_name,
        'account' : account,
        'path' : request.path,
    }

    return render(request, 'tag.html', context)


@require_http_methods(['GET'])
def hot(request):
    account = forms.checkAuth(request=request)
    page_obj = models.createPaginator(models.Question.objects.get_hot_questions(), request)

    context = { 
        'page_obj' : page_obj, 
        'tags' : models.Tag.objects.get_popular_tags(), 
        'best_members' : models.Profile.objects.get_five_best_members(), 
        'account' : account, 
        'path' : request.path 
    }

    return render(request, 'hot.html', context)


@login_required(login_url='/login/')
@require_http_methods(['GET'])
def log_out(request):
    continue_url = request.GET.get('continue')
    auth.logout(request)
    messages.success(request, 'Account has been logged out')

    if continue_url:
        return redirect(continue_url)
    

    return redirect('index')
