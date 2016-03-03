from django.shortcuts import render


def index(request):
    return render(request, 'lesson/index.html')


def lesson_detail(request):
    return render(request, 'lesson/lessondetail.html')
