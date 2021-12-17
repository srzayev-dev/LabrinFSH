from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Username')
    email = forms.EmailField(label="Email")
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Password Confirmation', widget = forms.PasswordInput)
    
    
    def clean(self):
        data = super().clean()
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError('Password confirmation does not match.')
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email is already in use')
        return data    



class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        user = User.objects.filter(email=self.cleaned_data['email']).first()
        if not user:
            raise forms.ValidationError('User does not exist')
        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError('Password is incorrect')
        return self.cleaned_data