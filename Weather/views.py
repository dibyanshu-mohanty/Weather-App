from django.shortcuts import render , redirect
import requests
from .models import city
from .forms import CityForm
# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3ec72171b250b5db22a26522d7638846"

    err_msg=''
    message=''
    message_class=''
    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']
            City_count=city.objects.filter(name=new_city).count()
            if City_count==0:
                response= requests.get(url.format(new_city)).json()
                if response['cod']==200:
                    form.save()
                else:
                    err_msg='City Doesnt Exist!'
            else:
                err_msg='City already exists in Database!'
        if not err_msg:
            message="City Added Successfully!"
            message_class="success"
        else:
            message=err_msg
            message_class="danger"
    form = CityForm()
    cities = city.objects.all()
    weather_list = []
    for City in cities:
        response= requests.get(url.format(City)).json()
        listings={
            'City':City.name,
            'temperature':response['main']['temp'],
            'description':response["weather"][0]['description'],
            'icon':response["weather"][0]['icon'],   
        }
        weather_list.append(listings)

    context={
        'weather_list':weather_list,
        'form': form,
        'message':message,
        'message_class':message_class,
    }
    return render(request,"Weather/Weather.html",context)

def delete_city(request,city_name):
         city.objects.get(name=city_name).delete()
         return redirect('home')