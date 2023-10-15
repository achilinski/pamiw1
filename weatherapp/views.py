from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .forms import CityNameForm

api_key = "vB8R8L0PDB7KaqANhXDy5Hi5zt66RhWG"


# Create your views here.
def index(request):
    return HttpResponse(
        "<a href='cities'>kutas</a></br><a href='cities_forecast'>Cities current conditions</a></br><a href='getLocation'>Search cities</a>")



def forecast(request, city_key):

    forecast = requests.get("http://dataservice.accuweather.com/currentconditions/v1/" + city_key,
                            params={"apikey": api_key})
    if not forecast.ok:
        return HttpResponse(forecast)
    forecast = forecast.json()
    body = "<html><body>"
    body += "<h1>Current conditions</h1>"
    body += "<ul>"
    body += "<li>Current temperature: " + str(
        forecast[0]['Temperature']['Metric']['Value']) + "</li>"
    body += "</ul>"


    forecast2 = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + city_key,
                            params={"apikey": api_key,"metric": "true"})
    if not forecast2.ok:
        return HttpResponse(forecast2)
    forecast2 = forecast2.json()

    body += "<h1>Tomorrow</h1>"
    body += "<ul>"
    body += "<li>Headline: " + forecast2['Headline']['Text'] + "</li>"
    body += "<li>Minimum Temperature: " + str(
        forecast2['DailyForecasts'][1]['Temperature']['Minimum']['Value']) + "</li>"
    body += "<li>Maximum Temperature: " + str(
        forecast2['DailyForecasts'][1]['Temperature']['Maximum']['Value']) + "</li>"
    body += "</ul>"

    forecast = requests.get("http://dataservice.accuweather.com/currentconditions/v1/" + city_key + "/historical/24/",
                            params={"apikey": api_key,"metric": "true"})
    if not forecast.ok:
        return HttpResponse(forecast)
    forecast = forecast.json()
    body += "<h1>Historical forecast</h1>"
    body += "<ul>"
    for hour in forecast:
        body += "<li>Time: " + str(hour['LocalObservationDateTime']) + "</li>"
        body += "<li>Weather: " + str(hour['WeatherText']) + "</li>"
        body += "<li>Temperature: " + str(hour['Temperature']['Metric']['Value']) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body)



def getLocation(request):
    form = CityNameForm
    context = {"form" : form}
    city_name = ""
    citiesList = ""
    if request.method == "POST":
        city_name = request.POST["city_name"]
        citiesList = requests.get("http://dataservice.accuweather.com/locations/v1/cities/autocomplete",
                                  params={"apikey": api_key,
                                          "q": city_name})
        citiesList = citiesList.json()
        return render(request, "search2.html", {'data' : citiesList,
                                                'form' : form})



    return render(request, "search.html", context)




