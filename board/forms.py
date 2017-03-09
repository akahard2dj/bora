from django import forms
from django.contrib.auth.models import User
from board.models import Post
from board.models import UserProfile



class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        exclude = ('category',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website',)

