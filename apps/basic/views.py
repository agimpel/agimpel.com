from django.shortcuts import render


def index(request):

    context = {
        'title': 'Home',
        'nav_title': [['home', None]],
    }

    return render(request, 'basic/index.html', context=context)



def about(request):

    context = {
        'title': 'About',
        'nav_title': [['about', None]],
    }

    return render(request, 'basic/about.html', context=context)




def contact(request):

    context = {
        'title': 'Contact',
        'nav_title': [['contact', None]],
    }

    return render(request, 'basic/contact.html', context=context)
