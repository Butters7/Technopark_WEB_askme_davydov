from . import models
from django.shortcuts import render

# Create your views here.
def ask(request):
    return render(request, 'ask.html')


def base(request):
    return render(request, 'base.html')


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')


def question(request, question_id):
    context = {'question': models.QUESTIONS[question_id]}
    return render(request, 'question.html', context)


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')

def tag(request):
    return render(request, 'tag.html')
