__author__ = 'jonathan'

from django import forms
from home.models import postulantes

class PostulantesForm(forms.ModelForm):
    class Meta:
        model = postulantes