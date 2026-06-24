from django import forms
from website.models import Contact, Question


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'category']