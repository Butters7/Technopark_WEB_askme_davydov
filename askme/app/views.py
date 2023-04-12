from . import models
from django.shortcuts import render

# Create your views here.
def ask(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'ask.html', context)


def base(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'base.html', context)


def index(request):
    context = {'questions': models.QUESTIONS, 'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'index.html', context)


def login(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'login.html', context)


def question(request, question_id):
    context = {'question': models.QUESTIONS[question_id], 'answers': models.ANSWERS, 'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'question.html', context)


def settings(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'settings.html', context)


def signup(request):
    context = {'tags': models.TAGS, 'bm': models.BEST_MEMBERS}
    return render(request, 'signup.html', context)

def tag(request):
    # context = {'tag': models.TAGS[tag_name]}
    return render(request, 'tag.html')
