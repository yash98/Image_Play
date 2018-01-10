from django import forms


class ImageUpload(forms.Form):
    image = forms.FileField()


class ImageConvert(forms.Form):
    rows = forms.IntegerField()
    cols = forms.IntegerField()
