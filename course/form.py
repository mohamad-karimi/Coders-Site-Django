from django import forms
from course.models import Score


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['name', 'email', 'score', 'comment']