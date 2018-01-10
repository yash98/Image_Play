from django import forms


class ImageUpload(forms.Form):
    image = forms.FileField()


class ImageConvert(forms.Form):
    cols = forms.IntegerField()
    rows = forms.IntegerField()
