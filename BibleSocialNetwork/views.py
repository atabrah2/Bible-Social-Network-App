from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'BibleSocialNetwork/index.html')


def graph(request):
    return render(request, 'BibleSocialNetwork/graph.html')


def rankings(request):
    return render(request, 'BibleSocialNetwork/rankings.html')


def graphtest(request):
    return render(request, 'BibleSocialNetwork/graphtest.html')


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
