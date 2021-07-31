import time
from flask import *
import requests

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

url = ('https://newsapi.org/v2/top-headlines?country=in&apiKey=SIKE')
api_key = "NO"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def get_news():
    response = requests.get(url)
    newsx = json.loads(response.text)
    return newsx

@app.route('/')
def frontpage():
    global refresh_cap
    refresh_cap = refresh_cap + 1
    global total
    total = total + 1
    if total == 1:
        global news
        news = get_news()
    elif refresh_cap == 4:
        news = get_news()
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
    complete_url = base_url + "appid=GETONEYOURSELF"+"&q=" + city
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
    return render_template('frontpage.html',city=city,news=news,f=fontsize,ct=current_temperature,cp=current_pressure,ch=current_humidity,cd=weather_description)

# Suvid Datta 2021
