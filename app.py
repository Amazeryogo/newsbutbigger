import time
from flask import *
import requests
from keys import *

app = Flask(__name__)

global refresh_cap
refresh_cap = 0
# if this hits 4, we ping newsapi to get us new json


global total
total = 0
#total views/refreshes done

global news
news = ""
# This is the cache to stop newsapi to brick my apikey ;)

# add new urls
global url 
global base_url
url = "https://newsapi.org/v2/top-headlines?apiKey=" + NEWS
base_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + WEATHER 

def get_news(urls):
    response = requests.get(urls)
    newsx = json.loads(response.text)
    return newsx

@app.route('/')
def frontpage():
    final_url = base_url
    x = request.args
    if x.get('country') is not None:
        country = x.get('country')
        final_url = url + "&q=" + country
        refresh_cap = 0
    if x.get('category') is not None:
        category = x.get('category')
        final_url = url + "&category=" + category
        refresh_cap = 0
    if x.get('sources') is not None:
        sources = x.get('sources')
        final_url = url + "&sources=" + sources
        refresh_cap = 0
    if x.get('from') is not None:
        from_date = x.get('from')
        final_url = url + "&from=" + from_date
        refresh_cap = 0
    if x.get('to') is not None:
        to_date = x.get('to')
        final_url = url + "&to=" + to_date
        refresh_cap = 0
    if x.get('domain') is not None:
        domain = x.get('domain')
        final_url = url + "&domain=" + domain
        refresh_cap = 0
    else:
        final_url = url + "&q=india"



    refresh_cap = refresh_cap + 1
    global total
    total = total + 1
    if total == 1:
        global news
        news = get_news(final_url)
    elif refresh_cap == 4:
        news = get_news(final_url)
        print(refresh_cap)
        refresh_cap = 0
    else:
        pass
    fontsize = request.args.get("fs")
    if fontsize == None:
       fontsize = 0


    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']


    hmmm = "https://geolocation-db.com/json/"+ip+"position=true"
    new = requests.get(hmmm).json()
    city = new['city']
    final_url = base_url + "&q=" + city
    response = requests.get(final_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature = round(current_temperature - 273.15, 1)
        far = (current_temperature * 9/5) + 32
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
    else:
        print(x)
    return render_template('frontpage.html',far=far,city=city,news=news,f=fontsize,ct=current_temperature,cp=current_pressure,ch=current_humidity,cd=weather_description)

# Suvid Datta 2021

app.run(debug=True)