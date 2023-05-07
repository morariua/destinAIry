# auth_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mainpage')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('login')

def mainpage(request):
    return render(request, 'mainpage.html')

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render
from django.http import HttpResponse
import json

def json_view(request):
    with open('chatgpt.json') as f:
        data = json.load(f)
    return HttpResponse(data)




#q: upload the json data to the google maps api?
# a: yes, you can add a new view to the views.py file and then add a new url to the urls.py file
#q: please write the code to link the json data to the google maps api
# a:    with open('chatgpt.json') as f:
#         data = json.load(f)
#     return HttpResponse(data)
#q: please write the code to link the json data to the google maps api
# a:    with open('chatgpt.json') as f:
#         data = json.load(f)
#     return HttpResponse(data)








# Path: auth_app/views.py



