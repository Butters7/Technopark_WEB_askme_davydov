from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import Http404
from app import models


def createPaginator(models, request):
    list_obj = models
    paginator = Paginator(list_obj, 3)
    page_number = request.GET.get('page')
    
    if not page_number:
        page_number = 1

        
    if int(page_number) > paginator.num_pages:
        page_number = paginator.num_pages

    page_obj = paginator.get_page(page_number)


    return page_obj
    


def get_context(page_obj=None, tags = None, best_members = None):
    return {'page_obj': page_obj, 'tags': tags, 'best_members': best_members }


def ask(request):
    context = get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'ask.html', context)


def base(request):
    context = get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'base.html', context)


def index(request):
    page_obj = createPaginator(models.Question.objects.get_news_question(), request)
    context = get_context(page_obj, models.Tag.objects.get_popular_tags(), models.Profile.objects.get_five_best_members())

    return render(request, 'index.html', context)


def login(request):
    context = get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'login.html', context)


def question(request, question_id):
    if not models.Question.objects.filter(pk=question_id):
        raise Http404(f'Question_id {question_id} does not exist')
    
    page_obj = createPaginator(models.Question.objects.get(pk=question_id).answer_set.all(), request)
    context = get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['question'] = models.Question.objects.get(pk=question_id)

    return render(request, 'question.html', context)


def settings(request):
    context = get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'settings.html', context)


def signup(request):
    context = get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'signup.html', context)


def tag(request, tag_name):
    if not models.Tag.objects.filter(name=tag_name):
        raise Http404(f'Tag {tag_name} does not exist')

    page_obj = createPaginator(models.Question.objects.get_question_with_special_tag(tag_name), request)
    context = get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['tag_name'] = tag_name

    return render(request, 'tag.html', context)


def hot(request):
    question_obj = models.Question.objects.get_hot_questions()
    page_obj = createPaginator(question_obj, request)
    context = get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'hot.html', context)
