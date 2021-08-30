from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import post, comment, contactus


class register(UserCreationForm):
    password2 = forms.CharField(label='password confirm again', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class blog_post(forms.ModelForm):
    Image = forms.ImageField(required=False)

    class Meta:
        model = post
        fields = ['heading', 'content', 'Image']
        exclude = ['date']


class find(forms.Form):
    sea = forms.CharField()

    class Meta:
        model = post


class contact(forms.ModelForm):
    class Meta:
        model = contactus
        fields = ['name', 'email', 'message']


class cmnt(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['txt', ]


