from django.shortcuts import render
from apps.gallery.models import Background

import random


def index(request):

    all_backgrounds = Background.objects.filter(show=True).all()

    number_backgrounds = len(all_backgrounds)
    try:
        i_background = random.randint(0, number_backgrounds-1)
        background_url = all_backgrounds[i_background].picture.url
        background_title = all_backgrounds[i_background].title
    except:
        i_background = 0
        background_url = ""
        background_title = "-"


    context = {
        'title': 'Home',
        'nav_title': [['home', None]],
        'background_urls': ',\n'.join(['\"%s\"' % bg.picture.url for bg in all_backgrounds]),
        'background_titles': ',\n'.join(['\"%s\"' % bg.title for bg in all_backgrounds]),
        'number_backgrounds': number_backgrounds,
        'i_background': i_background,
        'current_background': i_background+1,
        'background_url': background_url,
        'background_title': background_title,
    }

    return render(request, 'basic/index.html', context=context)



def about(request):

    context = {
        'title': 'About me',
        'nav_title': [['about me', None]],
    }

    return render(request, 'basic/about.html', context=context)




def imprint(request):

    context = {
        'title': 'Imprint',
        'nav_title': [['imprint', None]],
    }

    return render(request, 'basic/imprint.html', context=context)
