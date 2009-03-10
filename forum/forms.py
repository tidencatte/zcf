from django import forms
from forum.models import Post, PostRevision

class PostForm(forms.ModelForm):
	post_content = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = Post
		exclude = ("user", "thread", "posted")
