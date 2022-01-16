from flask import Flask, render_template, request
from datetime import datetime
import requests
from random import randint
import os
import wikipedia
import json

apod = 0
gtt = ""
w_api_key = "76ce09d339c3310433855fceee368b9d"
print(os.getcwd())
imgfolder = os.path.join('static', 'img')

app=Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = imgfolder

@app.route('/')
def form():
    return render_template('index.html', image = "src=" + os.path.join(app.config['UPLOAD_FOLDER'], "1x1.png"), focus = "autofocus")


@app.route('/', methods=['POST'])
def main():
    
    raw_input = request.form['variable']
    user_input = str(raw_input.lower())
    if "time" in user_input:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if "date" in user_input:
            now = datetime.now()
            current_date = now.strftime("%D")
            return  render_template('index.html', image = "src=" + os.path.join(app.config['UPLOAD_FOLDER'], "1x1.png"), wiki = " The current time is: " + current_time + "<br> And the current date is: " + current_date)
        else:
            return render_template('index.html', image = "src=" + os.path.join(app.config['UPLOAD_FOLDER'], "1x1.png"), wiki="The current time is: " + current_time)
    
    elif "date" in user_input:
        now = datetime.now()
        current_date = now.strftime("%D")
        return render_template('index.html', image = "src=" + os.path.join(app.config['UPLOAD_FOLDER'], "1x1.png"), wiki="The current date is: " + current_date)

    #--------------------------------Weather--------------------------------#
    elif "weather" in user_input.lower():
        if "in" in user_input:
            city = user_input.split("in")[0::]
            city_name = city[1]
        else:
            city_name = "Kourou"

        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + w_api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]

            current_temperature = y["temp"]
            # ----------------------------------------#
            celsius = current_temperature - 272, 15
            # ----------------------------------------#
            z = x["weather"]
            
            weather_description = z[0]["description"]
            if "cloud" in weather_description:
                weather_descriptionm = "clouds"
            elif "clear" in weather_description:
                weather_descriptionm = "clear"
            elif "rain" in weather_description:
                weather_descriptionm = "rain"
            elif "fog" or "mist" in weather_description:
                weather_descriptionm = "mist"

            w = weather_descriptionm + str(randint(1,3))+".png" 
            imgpath = os.path.join(app.config['UPLOAD_FOLDER'], w)
            
            return render_template('index.html', image = "src="+imgpath, wiki = "The current temperature in " + city_name + " is: " + str(celsius).replace('(', '')[:3] + "C°" + "<br>" + "The weather in " + city_name + " is: " + str(weather_description))
    #--------------------------------Weather--------------------------------#
    elif "search" in user_input:
        try:
            lowcase = str(user_input)
            data = lowcase.replace("search ", "")
            new = data.translate({ord(i): None for i in ' '})
            return render_template('index.html', wiki = wikipedia.summary(new, sentences=5), image = "src=" + os.path.join(app.config['UPLOAD_FOLDER'], "1x1.png"))
        except:
            return "Wikipedia page was not found" 

    elif "picture of the day" in user_input:
        global apod
        global gtt
        apod = 1
        f = r"https://api.nasa.gov/planetary/apod?api_key=XMqdRJg4lgeRUm0N1ETvfUvymjgmfhXJ7ot2Udgj"
        data = requests.get(f)
        gtt = json.loads(data.text)
        return render_template('index.html', wiki = "The astronomy picture of the day is: " + "<br> <b>" + gtt["title"] + " </b> <br> <br>" +
                                "Do you want to hear the explanation of this picture?", image = "src=" + gtt["url"])    
    return form()

if __name__ == '__main__':
    app.run(host="192.168.0.20", port=5000)