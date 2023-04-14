from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import Http404
from . import models


class createPaginator:
    def __init__(self, models, request):
        self.list_obj = models
        self.paginator = Paginator(self.list_obj, 3)
        self.page_number = request.GET.get('page')

        if not self.page_number:
            self.page_number = 1

        if int(self.page_number) > self.paginator.num_pages:
           self.page_number = self.paginator.num_pages

        self.page_obj = self.paginator.get_page(self.page_number)
    

    def getPageObj(self):
        return self.page_obj


def ask(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'ask.html', context)


def base(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'base.html', context)


def index(request):
    paginator = createPaginator(models.QUESTIONS, request)
    page_obj = paginator.getPageObj()

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
    
    paginator = createPaginator(models.ANSWERS, request)
    page_obj = paginator.getPageObj()

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
    
    paginator = createPaginator(models.QUESTIONS, request)
    page_obj = paginator.getPageObj()

    context = {'page_obj': page_obj, 'tags': models.TAGS, 'bm': models.BEST_MEMBERS, 'tag': tag_name}
    return render(request, 'tag.html', context)

def hot(request):
    paginator = createPaginator(models.HOT, request)
    page_obj = paginator.getPageObj()

    context = {'page_obj': page_obj, 'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'hot.html', context)
