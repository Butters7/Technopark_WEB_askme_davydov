from django.core.paginator import Paginator
from . import models
from django.shortcuts import render, redirect
from django.http import Http404

# Create your views here.
def ask(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'ask.html', context)


def base(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'base.html', context)


def index(request):
    question_list = models.QUESTIONS
    paginator = Paginator(question_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'index.html', context)


def login(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'login.html', context)


def question(request, question_id):
    try:
        question = models.QUESTIONS[question_id]
    except IndexError:
        raise Http404(f"Question with ID {question_id} not found")
    
    answer_list = models.ANSWERS
    paginator = Paginator(answer_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'question': question, 'page_obj': page_obj, 'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'question.html', context)


def settings(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'settings.html', context)


def signup(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'signup.html', context)

def tag(request, tag_name):
    tag = next((t for t in models.TAGS if t['tag_name'] == tag_name), None)

    if tag is None:
        raise Http404(f"Tag {tag_name} not found")
    
    tag_list = models.QUESTIONS
    paginator = Paginator(tag_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'tags': models.TAGS, 'bm': models.BEST_MEMBERS, 'tag': tag_name}
    return render(request, 'tag.html', context)

def hot(request):
    hot_list = models.HOT
    paginator = Paginator(hot_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'hot.html', context)
