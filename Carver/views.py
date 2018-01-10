from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ImageUpload, ImageConvert
import subprocess
from PIL import Image


def index(request):
    request.session.save()
    uploadform = ImageUpload()
    convertform = ImageConvert()

    if 'uploaded' not in request.session:
        request.session['uploaded'] = False
        request.session['reso'] = False
        request.session['ImageReady'] = False
    else:
        try:
            im = Image.open("media/"+str(request.session.session_key)+"/"+str(request.session.session_key))
            request.session['reso'] = im.size
        except (FileNotFoundError, OSError):
            im = None
            request.session['reso'] = (0,0)


    if 'name' not in request.session:
        request.session['name'] = 'output'

    if 'upload' in request.POST and request.FILES:
        myfile = request.FILES['image']
        request.session['name'] = myfile.name
        subprocess.call(['rm', '-rf', "media/"+str(request.session.session_key)+"/"])
        fs = FileSystemStorage(location="media/"+str(request.session.session_key))
        filename = fs.save(str(request.session.session_key), myfile)
        # uploaded_file_url = fs.url(filename)
        try:
            im = Image.open("media/"+str(request.session.session_key)+"/"+str(request.session.session_key))
        except OSError:
            return render(request, 'Carver/index.html', {'uploadform': uploadform, 'convertform': convertform,
                                    'uploaded': request.session['uploaded'],
                                    'reso': request.session['reso'],
                                    'ImageReady': request.session['ImageReady']})

        request.session['reso'] = im.size
        request.session['uploaded_file_url'] = "media/"+str(request.session.session_key)+"/"+str(request.session.session_key)
        request.session['uploaded'] = True
        return render(request, 'Carver/index.html', {'uploadform': uploadform,
                                                     'uploaded_file_url': request.session['uploaded_file_url'],
                                                     'convertform': convertform, 'uploaded': request.session['uploaded'],
                                                     'reso': request.session['reso']})

    if request.session['uploaded']:
        if 'convert' in request.POST:
            cols = request.POST.get('cols')
            rows = request.POST.get('rows')
            name = request.session['name']
            convertform = ImageConvert(request.POST)
            if convertform.is_valid():
                subprocess.call(['java','-jar', 'seamcarving.jar',
                                 'media/'+str(request.session.session_key)+'/'+str(request.session.session_key),
                                 str(rows), str(cols), str(request.session.session_key), request.session['name']])
                request.session['ImageReady'] = 'media/'+str(request.session.session_key)+'/'+request.session['name']
            return render(request, 'Carver/index.html', {'convertform': convertform, 'uploadform': uploadform,
                                                         'uploaded_file_url': request.session['uploaded_file_url'], 'rows': rows,
                                                         'cols': cols, 'uploaded': request.session['uploaded'],
                                                         'reso': request.session['reso'],
                                                         'ImageReady': request.session['ImageReady']})

    return render(request, 'Carver/index.html', {'uploadform': uploadform, 'convertform': convertform,
                                                 'uploaded': request.session['uploaded'],
                                                 'reso': request.session['reso'],
                                                 'ImageReady': request.session['ImageReady']})

