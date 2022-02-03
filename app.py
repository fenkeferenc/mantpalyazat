from flask import Flask, render_template, request
from datetime import datetime
import requests
from random import randint
import os
import wikipedia
import json
from geopy import Nominatim
import reverse_geocoder as rg
from countryconvert import get_country_name
from news import news

apod = 0
gtt = ""
w_api_key = "76ce09d339c3310433855fceee368b9d"
print(os.getcwd())
imgfolder = os.path.join('static', 'img')
app=Flask(__name__,template_folder='templates')
app.secret_key = 'Øæw]:©p²T¶8ÛMU;'
app.config['UPLOAD_FOLDER'] = imgfolder
blankimg = "<img src=" + os.path.join(app.config['UPLOAD_FOLDER'], "1x1.png")+">"
geoapp = Nominatim(user_agent="Userid18479627")

def Geocode(cord):
    result = rg.search(cord)
    return result

def img(x):
    if "youtube" in x:
        return "<iframe src=" + os.path.join(x)+' allow="autoplay; encrypted-media">'     
    else:
        return "<img src=" + os.path.join(x)+'>'

@app.route('/')
def form():
    home = render_template('index.html', image = "<img src=" + os.path.join(app.config['UPLOAD_FOLDER'], "epic" + str(randint(1,3)) +".jpg")+">", 
    wiki= "<br> + date/time <br> + weather <br> + weather on the Mars <br> + Picture of the day *on [Year-Month-Day]* <br> + International Space Station, ISS <br> + Search (using wikipedia) *title* <br> + News(Latest space exploration news)", TextTitle = "<h1> The keyword list </h1>")
    return home

@app.route('/frame')
def frame():
    return render_template('widget.html')


@app.route('/', methods=['POST'])
def main():
    global apod
    global gtt
    raw_input = request.form['variable']
    user_input = str(raw_input.lower())
    if apod == 1:
        print("apod = 1")
        if "yes" in user_input:
            print("yes")
            explain = gtt["explanation"].split(".")[0:3]
            apod = 0
            out = ""
            for i in range(0,len(explain)):
                out += explain[i] + "."
            return render_template('index.html', image = img(gtt["url"]), wiki = out)
        elif "no" in user_input:
            apod = 0
            return render_template('index.html', wiki = "Okay.")
        else:
            apod = 1
            return render_template('index.html', image = img(gtt["url"]), wiki = "Answer with yes or no please!")

    elif "time" in user_input:
        if "in" in user_input:
            city = user_input.split("in")[0::]
            

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if "date" in user_input:
            now = datetime.now()
            current_date = now.strftime("%D")
            return  render_template('index.html', wiki = " The current time is: " + current_time + "<br> And the current date is: " + current_date)
        else:
            return render_template('index.html', wiki="The current time is: " + current_time)
    
    elif "home" in user_input:
        return form()

    elif "date" in user_input:
        now = datetime.now()
        current_date = now.strftime("%D")
        return render_template('index.html', wiki="The current date is: " + current_date)

    elif "weather" in user_input and "mars" in user_input:
        f = r"https://api.maas2.apollorion.com"
        response = requests.get(f)
        result = json.loads(response.text)
        min_temp = int(result["min_temp"])
        max_temp = int(result["max_temp"])
        avg_temp = (min_temp + max_temp)/2
        avg_temp = str(avg_temp)
        t = str(result["terrestrial_date"])
        pressure = str(result["pressure"])
        opacity = str(result["atmo_opacity"])
        sol = str(result["sol"])
        timestamp = str(t.split("T")[0])
        return render_template('index.html', wiki="The average temperature on Mars in this month was: <br>"+ avg_temp + "C <br><br>" +
                                "The weather according to the opacity of the atmosphere is: <br>" + opacity + "<br><br>" + 
                                "Average atmospheric pressure: <br>" + pressure + " Pascal <br><br>" +
                                "This was the " + sol +". "+"report since 2012-08-07" +"<br>"+
                                "Updated on: " + timestamp,
                                image = img("/static/img/rover1.png"))


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
            
            return render_template('index.html', image = img(imgpath), wiki = "The current temperature in " + city_name + " is: " + str(celsius).replace('(', '')[:3] + "C°" + "<br>" + "The weather in " + city_name + " is: " + str(weather_description))
    #--------------------------------Weather--------------------------------#
    elif "search" in user_input:
        try:
            lowcase = str(user_input)
            data = lowcase.replace("search ", "")
            data = data.replace("for", "")
            new = data.translate({ord(i): None for i in ' '})
            return render_template('index.html', wiki = wikipedia.summary(new, sentences=5))
        except:
            return "Wikipedia page was not found" 

    elif "picture of the day" in user_input:
        if "on" in user_input:
            apod = 1
            on = user_input.split("on ")[0::]
            print("onstrip", on)
            on = on[1]
            print(on)
            f = r"https://api.nasa.gov/planetary/apod?api_key=XMqdRJg4lgeRUm0N1ETvfUvymjgmfhXJ7ot2Udgj"
            params = "date=" + on
            data = requests.get(f,params=params)
            gtt = json.loads(data.text)
            print(gtt)
            return render_template('index.html', wiki = "The astronomy picture on " + on + "was: " + "<br> <b>" + gtt["title"] + " </b> <br> <br>" +
                                    "Do you want to hear the explanation of this picture?", image = img(gtt["url"]))

        elif "on" not in user_input:
            apod = 1
            f = r"https://api.nasa.gov/planetary/apod?api_key=XMqdRJg4lgeRUm0N1ETvfUvymjgmfhXJ7ot2Udgj"
            data = requests.get(f)
            gtt = json.loads(data.text)
            return render_template('index.html', wiki = "The astronomy picture of the day is: " + "<br> <b>" + gtt["title"] + " </b> <br> <br>" +
                                    "Do you want to hear the explanation of this picture?", image = img(gtt["url"]))
        
    elif "international space station" in user_input or "iss" in user_input:
        data = requests.get("http://api.open-notify.org/iss-now.json")
        iss = json.loads(data.text)
        lat = iss['iss_position']['latitude']
        long = iss['iss_position']['longitude']
        print(lat)
        print(long)
        cords =(lat, long)
        pos = Geocode(cords)
        pos = dict(pos[0])
        print(pos)
        state = pos.get("name")
        country = pos.get("cc")
        country = str(get_country_name(country))
        position = "The International Space Station is currently over " + state + " in " + country
        return render_template('index.html', wiki=position, image='<iframe src="frame"></iframe>')

    elif "news" in user_input:
        title, summary, url, imgurl, = news()[0], news()[1], news()[2], news()[3]
        return render_template('index.html', TextTitle="<h1>"+ '<a href="'+url+'">'  + title + "</a></h1>" + "<br>", wiki=summary, image='<img src="' + imgurl + '">'+'</a>',)

    return form()

if __name__ == '__main__':
    app.run(host="localhost", port=5000)