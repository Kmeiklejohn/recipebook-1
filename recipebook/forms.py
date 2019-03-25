from django import forms
from recipebook.models import Author


class AddAuthor(forms.Form):
    name = forms.CharField(label='Author Name', max_length=100)
    bio = forms.CharField(widget=forms.Textarea, label='bio')
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput)


class AddRecipe(forms.Form):

    title = forms.CharField(label='Recipe Title', max_length=100)
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(), label='Author')
    description = forms.CharField(max_length=150, label="Description")
    time = forms.IntegerField(label='Prep Duration')
    instructions = forms.CharField(widget=forms.Textarea, label="Instructions")


class LoginForm(forms.Form):
    username = forms.CharField(label='Login Name', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
