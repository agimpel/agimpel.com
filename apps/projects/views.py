from django.shortcuts import render


def index(request):

    context = {
        'title': 'Projects',
        'nav_title': [['projects', None]],
    }

    return render(request, 'projects/index.html', context=context)
