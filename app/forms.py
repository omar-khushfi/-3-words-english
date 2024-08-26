from django import forms
from .models import *


class wordform(forms.ModelForm):
    class Meta:
        model=Word;
        fields=[
            'arabic',
            'english',
        ]
        widgets= {
        'arabic':forms.TextInput(attrs={'class':'form-control'}),
        'english':forms.TextInput(attrs={'class':'form-control'}),
        }