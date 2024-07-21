from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from .decorators import unauthenticated_user
from django.contrib import messages
import requests

@unauthenticated_user
def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = email.split('@')[0]
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_exist = User.objects.filter(username=username).first()
        if user_exist:
            messages.info(request, 'Email has already been taken.')
            return redirect('signuppage')
        elif password1 != password2:
            messages.info(request, 'Passwords did not match.')
            return redirect('signuppage')
        else:
            user_obj = User.objects.create_user(username, email=email, first_name=firstname, last_name=lastname, password=password1)
            messages.info(request, f'Account has been created for Mr. {user_obj.username}')
            return redirect('loginpage')
    context = {}
    return render(request, 'projectapp/signuppage.html', context)

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.info(request, 'User not found.')
            return redirect('loginpage')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.info(request, 'Please enter the credentials correctly.')
                return redirect('loginpage')
            else:
                login(request, user)
                return redirect('home')            
    context = {}
    return render(request, 'projectapp/loginpage.html', context)

def logout_view(request):
    logout(request)
    return redirect('loginpage')

@login_required(login_url='signup/')
def home(request):
    city = request.GET.get('cityname')
    apiKey = '&appid=4cca393564b02a7a8a22538f9df73475'
    url = f'https://api.openweathermap.org/data/2.5/weather?units=metric&q={city}{apiKey}'
    print(city)
    weather_icon = static(f"images/default.jpg")
    if city:
        try:
            data = requests.get(url).json()
            area = data.get('name') + ', ' + data['sys']['country']
            weather_name = data['weather'][0]['main']
            weather_icon = static(f"images/{weather_name}.jpg")
            temp = round(data['main']['temp'])
            humid = data['main']['humidity']
            wind = round(data['wind']['speed'])
            desc = data['weather'][0]['description']
            data_available = True
        except Exception as e:
            print(f"Error: {e}")
            messages.info(request, 'City not found.')
            return redirect('home')
    else:
        data_available = False
        area = ''
        temp = ''
        humid = ''
        wind = ''
        desc = ''
        print(city)
    context = {
        'city': area,
        'temperature': temp,
        'humidity': humid,
        'wind_speed': wind,
        'description': desc,
        'weather': weather_icon,
        'data': data_available,
    }
    return render(request, 'projectapp/home.html', context)