from django import forms
from blog.models import Comment, ReplayComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'email', 'comment']

class ReplayCommentForm(forms.ModelForm):
    class Meta:
        model = ReplayComment
        fields = ['comment']