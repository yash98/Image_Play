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

This is a content-aware image resizing web app. It reduces the resolution of the image without affecting the content which is most noticable. Unlike other standard content-agnostic resizing techniques (e.g. cropping and scaling), the aspect ratio of the most interesting objects of the image does not change. 

It apply some simple shortest path algorithms and convert the whole picture into a graph and then determines a path from top to bottom (if a coloumn is being removed) which sum upto to minimum rgb value change and then remove the complete row.
