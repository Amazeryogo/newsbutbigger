import time
from flask import *
import requests

app = Flask(__name__)

url = ('https://newsapi.org/v2/top-headlines?country=in&apiKey=28747323d8ca4c64bc95ac313b7c269c')


@app.route('/')
def frontpage():
    response = requests.get(url)
    news = json.loads(response.text)
    fontsize = request.args.get("fs")
    if fontsize == None:
       fontsize = 0
    print(fontsize)
    return render_template('frontpage.html',news=news,f=fontsize)
