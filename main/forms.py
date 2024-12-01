from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class EmailPostForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    recipient = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)