from django import forms

class UploadForm(forms.Form):
    token = forms.CharField(max_length=100);
    uploadFile = forms.FileField()
