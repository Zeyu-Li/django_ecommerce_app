from django.shortcuts import render

# Create your views here.

def home(request):
    ''' homepage '''

    keywords = {"page": "home"}
    return render(request, 'shop/home.html', keywords)


def home_redirect(request):
    ''' redirect to home '''

    return redirect('home')
