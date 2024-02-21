from django.shortcuts import render

# Create your views here.
def index(request):
    pesanans = []
    return render(request, 'index.html', locals())