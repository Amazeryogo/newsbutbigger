import time
from flask import *
import requests

app = Flask(__name__)

url = ('https://newsapi.org/v2/top-headlines?country=in&apiKey=NO!')
api_key = "LOL SIKE"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

@app.route('/')
def frontpage():
    response = requests.get(url)
    news = json.loads(response.text)
    fontsize = request.args.get("fs")
    if fontsize == None:
       fontsize = 0
    #print(fontsize)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    hmmm = "https://geolocation-db.com/json/"+ip+"position=true"
    new = requests.get(hmmm).json()
    city = new['city']
    complete_url = base_url + "appid=NO"+"&q=" + city
    response = requests.get(complete_url)
    x = response.json()
    print(x)
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
    return render_template('frontpage.html',city=city,news=news,f=fontsize,ct=current_temperature,cp=current_pressure,ch=current_humidity,cd=weather_description)
