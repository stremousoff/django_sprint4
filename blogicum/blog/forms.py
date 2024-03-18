from blog.models import Comment, Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'location', 'pub_date', 'image')
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('author', 'post', 'is_published')
