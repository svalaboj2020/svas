from django import forms
from testapp.models import *

class enquiry_form(forms.Form):
    name=forms.CharField()
    phone=forms.CharField()
    email=forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class SM_upload_form(forms.ModelForm):
    class Meta:
        model=SM_upload
        fields='__all__'

class Rlink_upload_form(forms.ModelForm):
    class Meta:
        model=Rlink_upload
        fields='__all__'
