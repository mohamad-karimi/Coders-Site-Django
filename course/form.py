from django import forms
from course.models import Score, Comment


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'comment']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']