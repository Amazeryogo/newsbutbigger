import pyttsx3
import requests
import json
import time
from flask import *

app = Flask(__name__)

url = ('https://newsapi.org/v2/top-headlines?country=in&apiKey=SIKE')


@app.route('/')
def frontpage():
	try:
	   response = requests.get(url)
	except:
	    print("can, t access link, plz check you internet ")

    news = json.loads(response.text)
    fontsize = request.args.get("fs")
    if fontsize == None:
        fontsize = 0
    print(fontsize)
    return render_template('frontpage.html',news=news,f=fontsize)
