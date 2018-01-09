from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.conf  import  settings
from django.core.files.storage import FileSystemStorage
from .forms import ImageUpload
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
    if request.method == 'POST' and request.FILES:
        myfile = request.FILES['myfile']
        rows = request.POST['Row_pixels']
        cols = request.POST['Col_pixels']
        name = myfile.name
        fs = FileSystemStorage(location="media/"+str(request.session.session_key))
        filename = fs.save(str(request.session.session_key), myfile)
        uploaded_file_url = fs.url(filename)


        return render(request, 'Carver/index.html', {'uploaded_file_url':uploaded_file_url,
                                                     'rows':rows,'cols':cols})
    if request.method == 'POST':

        converting = True
        # subprocess.call(["pwd"])
        # subprocess.call(["ls"])
        #subprocess.call(['javac', 'Picture.java'])
        #os.system("javac SeamCarver.java")
        subprocess.call(['java','-jar','SeamCarving.jar','media/'+str(request.session.session_key)+'/'+str(request.session.session_key), str(rows), str(cols),'output.jpg'])
        # subprocess.call(['javac','SeamCarver.java'])
        # subprocess.call(['java', 'SeamCarver', '/media'+str(request.session.session_key)+'/'+str(request.session.session_key), str(rows), str(cols)])
        print('../media/'+str(request.session.session_key)+'/'+str(request.session.session_key))
        return render(request, 'Carver/index.html', {'uploaded_file_url':uploaded_file_url,
                                                     'rows':rows,'cols':cols,
                                                     'converting':converting})
    return render(request, 'Carver/index.html')

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