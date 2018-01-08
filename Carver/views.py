from django.shortcuts import get_object_or_404, render
from .models import image

def index(request):
    return render(request, 'Carver/index.html')
