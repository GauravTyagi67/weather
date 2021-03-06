from django.shortcuts import render
from django.http import HttpResponse
from darksky import forecast
from datetime import date,timedelta,datetime
from ipstack import GeoLookup
import requests
import json


# Create your views here.
#boston = forecast(key, 42.3601, -71.0589)


def home(request):	
	geo_lookup = GeoLookup("ba3495a30c658700b23916512f93eef0")

	location = geo_lookup.get_own_location()
	lat=location['latitude']
	lng=location['longitude']
	region=location['region_name']

	city = lat, lng

	weekday=date.today()
	weekly_weather={}
	hourly_weather={}

	with forecast('af01e6071f266c8191d8446298b7f097',*city) as city:
		for day in city.daily:
			day=dict(day=date.strftime(weekday,'%A'),sum=day.summary,tempMin=round(day.temperatureMin),tempMax=round(day.temperatureMax))

			weekday += timedelta(days=1)

			# weekly_weather={}

			pic=''
			summary=('{sum}'.format(**day).lower())

			if 'drizzle' in summary:
				pic='rain.png'
			elif 'rain' in summary:
				pic='rain.png'
			elif 'clear' in summary:
				pic='sun.png'
			elif 'partly cloudy' in summary:
				pic='partly-cloudy-day.png'
			else:
				pic='clouds.png'

			weekly_weather.update({'{day}'.format(**day):{'tempMin':'{tempMin}'.format(**day),'tempMax':'{tempMax}'.format(**day)}})
			weekday+=timedelta(days=1)

	today=weekly_weather[(date.today().strftime("%A"))]
	del weekly_weather[(date.today().strftime("%A"))]

	hour=datetime.now().hour
	location=forecast('af01e6071f266c8191d8446298b7f097',lat, lng)
	i=0
	

	while hour < 24:
		hour_=''
		temp=round(location.hourly[i].temperature)
		pic=''
		summary=location.hourly[i].summary.lower()

		if 'drizzle' in summary:
			pic='rain.png'
		elif 'rain' in summary:
			pic='rain.png'
		elif 'clear' in summary:
			pic='sun.png'
		elif 'partly cloudy' in summary:
			pic='partly-cloudy-day.png'
		else:
			pic='clouds.png'

		if hour < 12:
			hour_='{}am'.format(hour)
			hourly_weather.update({hour_:{'pic':pic,'temp':temp}})
		else:
			hour_='{}pm'.format(hour-12)
			hourly_weather.update({hour_:{'pic':pic,'temp':temp}})
		hour+=1
		i+=1
	return render(request,"home.html",{'weekly_weather':weekly_weather,'hourly_weather':hourly_weather,'region':region})