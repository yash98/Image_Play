from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from .models import Image
from .forms import UploadForm


def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UploadForm()
    return render(request, 'Carver/index.html', {'form': form})
