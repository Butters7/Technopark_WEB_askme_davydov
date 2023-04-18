from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import Http404


class createPaginator:
    pass


def ask(request):
    return render(request, 'ask.html')


def base(request):
    return render(request, 'base.html')


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def question(request, question_id):
    return render(request, 'question.html')


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')


def tag(request, tag_name):
    return render(request, 'tag.html')


def hot(request):
    return render(request, 'hot.html')
