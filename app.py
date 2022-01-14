from flask import Flask, render_template, request
from datetime import datetime
import requests
from random import randint
import os


w_api_key = "76ce09d339c3310433855fceee368b9d"
print(os.getcwd())
imgfolder = os.path.join('static', 'img')

app=Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = imgfolder

@app.route('/')
def form():
    return render_template('index.html')

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
            return "The current time is: " + current_time + "<br> And the current date is: " + current_date + form()
        else:
            return "The current time is: " + current_time + form()
    
    elif "date" in user_input:
        now = datetime.now()
        current_time = now.strftime("%D")
        return "The current date is:" + current_time + form()

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
                weather_description = "clouds"
                
            w = weather_description + str(randint(1,3))+".png" 
            imgpath = os.path.join(app.config['UPLOAD_FOLDER'], w)
            
            return "<p> The current temperature in " + city_name + " is: " + str(celsius).replace('(', '')[:3] + "C° \n The weather in " + city_name + " is: " + str(weather_description)+"</p>" + render_template('index.html', image = imgpath)

    return form()

if __name__ == '__main__':
    app.run(host="192.168.0.13", port=5000)