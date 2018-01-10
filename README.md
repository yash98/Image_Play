# Image_Play
> A Django based Webapp which uses Seam Carving to reduce resolution

## How to use on localhost?
1. git clone https://github.com/yash98/Image_Play.git
2. pip install -r requirement.txt
  (in virtual envirnment or globally)
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py runserver
### local server will start at http://127.0.0.1:8000/

### Description:

This is a content-aware image resizing web app where the image is reduced in size. Unlike standard content-agnostic resizing techniques (e.g. cropping and scaling), the most interesting features (aspect ratio, set of objects present, etc.) of the image are preserved. The image is reduced to the desired size entered by user without distortion for display.  

