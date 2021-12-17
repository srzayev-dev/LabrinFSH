from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect
from users.forms import UserLoginForm, UserRegisterForm
from django.contrib import auth

User = get_user_model()

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data.get('email')).first()
            login(request,user)
            return redirect('home')
        print(form.errors)
    else:
        form = UserLoginForm()


    return render(request, 'login.html', {'form':form})



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username = form.cleaned_data.get('username'),
                email = form.cleaned_data.get('email'),   
            )
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    context = {
        'form' : form,
    }
    return render(request, 'register.html', context=context)


def logout_view(request):
    auth.logout(request)
    return redirect('home')