from django.contrib.auth import authenticate
from django import forms

from utils import TemplatedForm

class LoginForm(TemplatedForm):
    email = forms.EmailField(
        required=True,
        max_length=75)
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        required=True,
        label="Password")

    def clean(self):
        if 'email' in self.cleaned_data \
               and 'password' in self.cleaned_data:
            user = authenticate(username=self.cleaned_data['email'],
                                password=self.cleaned_data['password']) 
            if not user or not user.is_authenticated():
                raise forms.ValidationError('Your login details '
                                        'are incorrect')
        return self.cleaned_data
    
    def save(self):
        user = authenticate(username=self.cleaned_data['email'],
                            password=self.cleaned_data['password']) 
        return user
    
