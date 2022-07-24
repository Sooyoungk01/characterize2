from django import forms
from .models import Images

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Images
        fields = ('id_ch', 'image')

# class UploadFileForm(forms.Form):
#     file = forms.FileField()
#
