from django import forms

class ImageUpload(forms.Form):
    image = forms.FileField()
    rows = forms.IntegerField()
    cols = forms.IntegerField()