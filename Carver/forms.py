from django import forms
from .models import Image


class UploadForm(forms.Form):
    class Meta:
        model = Image

    fields = ('photo',)
