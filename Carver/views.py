from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.conf  import  settings
from django.core.files.storage import FileSystemStorage
from .forms import ImageUpload, ImageConvert
import subprocess, os

# def index2(request):
#     if request.method == 'POST':
#         image_form = UploadForm(data = request.POST, files = request.FILES)
#         if image_form.is_valid():
#             # file is saved
#
#             return render(request, 'Carver/index.html', {'form': image_form})
#     else:
#         form = UploadForm()
#     return render(request, 'Carver/index.html')


def index(request):
    rows = 0
    cols = 0
    myfile=None
    name = None
    uploaded_file_url = None
    request.session.save()
    uploadform = ImageUpload()
    convertform = ImageConvert()

    if 'uploaded' not in request.session:
        request.session['uploaded'] = False

    if 'upload' in request.POST and request.FILES:
        myfile = request.FILES['image']
        name = myfile.name
        subprocess.call(['rm', '-rf', "media/"+str(request.session.session_key)+"/"])
        fs = FileSystemStorage(location="media/"+str(request.session.session_key))
        # filename = fs.save(str(request.session.session_key), myfile)
        # uploaded_file_url = fs.url(filename)
        uploaded_file_url = "media/"+str(request.session.session_key)+"/"+str(request.session.session_key)
        request.session['uploaded'] = True
        print(str(request.session.session_key))
        return render(request, 'Carver/index.html', {'uploadform': uploadform, 'uploaded_file_url': uploaded_file_url,
                                                     'uploaded': request.session['uploaded']})

    if request.session['uploaded']:
        if 'convert' in request.POST:
            convertform = ImageConvert(request.POST)
            if convertform.is_valid():
                subprocess.call(['java','-jar', 'SeamCarving.jar',
                                 'media/'+str(request.session.session_key)+'/'+str(request.session.session_key),
                                 str(rows), str(cols), name])
                print('media/'+str(request.session.session_key)+'/'+str(request.session.session_key))

            return render(request, 'Carver/index.html', {'convertform': convertform, 'uploadform': uploadform,
                                                         'uploaded_file_url': uploaded_file_url, 'rows': rows,
                                                         'cols': cols, 'uploaded': request.session['uploaded']})

    return render(request, 'Carver/index.html', {'uploadform': uploadform, 'convertform': convertform,
                                                 'uploaded': request.session['uploaded']})

# def index(request):
#     if request.method=="POST" and request.FILES['myfile']:
#         image = ImageUpload(request.POST)
#         if image.is_valid():
#             cd = image.cleaned_data
#             fs = FileSystemStorage()
#             filename = fs.save(cd['image'].name, cd['image'])
#             return render(request, 'Carver/index.html',{'form':image})
#     else:
#         image = ImageUpload()
#     return (request,'Carver/index.html',{'form':image})
