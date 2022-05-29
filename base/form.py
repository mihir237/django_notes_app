from dataclasses import field
from django.forms import ModelForm
from .models import Lable, Note


class LableForm(ModelForm):
    class Meta:
        model = Lable
        fields = '__all__'


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['note']
