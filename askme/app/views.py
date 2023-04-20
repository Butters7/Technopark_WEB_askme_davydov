from django.shortcuts import render, redirect
from django.http import Http404
from app import models    


def ask(request):
    context = models.get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'ask.html', context)


def base(request):
    context = models.get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'base.html', context)


def index(request):
    page_obj = models.createPaginator(models.Question.objects.get_news_question(), request)
    context = models.get_context(page_obj, models.Tag.objects.get_popular_tags(), models.Profile.objects.get_five_best_members())

    return render(request, 'index.html', context)


def login(request):
    context = models.get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'login.html', context)


def question(request, question_id):
    if not models.Question.objects.filter(pk=question_id):
        raise Http404(f'Question_id {question_id} does not exist')
    
    page_obj = models.createPaginator(models.Question.objects.get(pk=question_id).answer_set.all(), request)
    context = models.get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['question'] = models.Question.objects.get(pk=question_id)

    return render(request, 'question.html', context)


def settings(request):
    context = models.get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'settings.html', context)


def signup(request):
    context = models.get_context(tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'signup.html', context)


def tag(request, tag_name):
    if not models.Tag.objects.filter(name=tag_name):
        raise Http404(f'Tag {tag_name} does not exist')

    page_obj = models.createPaginator(models.Question.objects.get_question_with_special_tag(tag_name), request)
    context = models.get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())
    context['tag_name'] = tag_name

    return render(request, 'tag.html', context)


def hot(request):
    question_obj = models.Question.objects.get_hot_questions()
    page_obj = models.createPaginator(question_obj, request)
    context = models.get_context(page_obj=page_obj, tags=models.Tag.objects.get_popular_tags(), best_members=models.Profile.objects.get_five_best_members())

    return render(request, 'hot.html', context)
