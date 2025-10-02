from django import forms
from django.contrib.auth.models import User
from Blog.models import Blog

class UserRegForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["first_name","username","password","email"]

        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    options=(
        ('reader','reader'),('writer','writer')
    )
    usertype=forms.ChoiceField(choices=options,widget=forms.Select(attrs={'class':'form-select'}))

class CreateForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=["title","content","blog_pic"]

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
            
        }