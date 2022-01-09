try:
    from tkinter import *
except:
    from _tkinter import *
from datetime import datetime
import requests
import wikipedia
import webbrowser
import json
import os
from random import randint

# ---------------------------------Backend---------------------------------#
#-------------------VARIABLE-------------------#
w_api_key = "76ce09d339c3310433855fceee368b9d"
final_output = ""
count = 0
apod = 0
gtt = ""
os.chdir(os.path.dirname(__file__))
name = ""
count_name = 0
#-------------------VARIABLE-------------------#

# --------------FUNTCION------------------#
def enter(event=None):
    ()
# --------------------------------#
def weatherimg():
    global ImgWindow
    global count
    r = str(randint(1, 3))
    img = PhotoImage(weather_description + r + ".png")
    ImgWindow.configure(file=img)
    count = count + 1

def help():
    helpwindow = Toplevel(root)
    helpwindow.geometry("450x403+912+158")
    helpwindow.resizable(width=FALSE, height=FALSE)
    helptext = Label(helpwindow,
                     text="Keyword list: \n date \n time \n weather \n search \n picture of the day \n Where am i/Where are we etc... \n Search *your word*",
                     fg="black", bd=35, font=("Arial", 20))
    helptext.pack()

def output(x):
    global chatWindow
    chatWindow.configure(text=x)
    messageWindow.delete(0, "end")
# --------------FUNTCION------------------#

#---------------------------MAIN---------------------------#
def main():
    global count
    global ImgWindow
    user_input = str(raw_input.get()).lower()    

    if count > 0:
        count = 0
        ImgWindow.blank()

    if "time" in user_input.lower():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if "date" in user_input.lower():
            now = datetime.now()
            current_date = now.strftime("%D")
            output("The current time is: " + current_time + "\n"
                                                            "And the current date is: " + current_date)
        else:
            output("The current time is: " + current_time)


    elif "date" in user_input.lower():
        now = datetime.now()
        current_time = now.strftime("%D")
        output("The current date is:" + current_time)

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
            global weather_description
            weather_description = z[0]["description"]
            output(" The current temperature in " + city_name + " is: " + str(celsius).replace('(', '')[:3] + "C"
                                                                                                              "\n The weather in " + city_name + " is: " + str(
                weather_description))

            if "rain" in weather_description:
                weather_description = "rain"
                weatherimg()

            elif "cloud" in weather_description:
                weather_description = "clouds"
                weatherimg()
            elif "clear sky" in weather_description:
                weather_description = "clear"
                weatherimg()
            else:
                pass

        else:
            output(" City Not Found ")
    #--------------------------------Weather--------------------------------#

    elif "search" in user_input.lower():
        try:
            lowcase = str(user_input.lower())
            data = lowcase.replace("search ", "")
            new = data.translate({ord(i): None for i in ' '})
            output(wikipedia.summary(new, sentences=5))
        except:
            output("Wikipedia page was not found")


    elif "lang" in user_input.lower():
        wikipedia.set_lang(user_input[5:])
        output("language succesfully set to " + user_input[5:])

    #-------------------------APOD-------------------------#
    elif "picture of the day" in user_input or user_input == "apod":
        chatWindow.config(font=("Castellar", 15))
        global apod
        global gtt
        apod = 1
        f = r"https://api.nasa.gov/planetary/apod?api_key=XMqdRJg4lgeRUm0N1ETvfUvymjgmfhXJ7ot2Udgj"
        data = requests.get(f)
        gtt = json.loads(data.text)
        output("The astronomy picture of the day is: \n" + gtt[
            "title"] + "\n Do you want to hear the explanation of this picture?")
        webbrowser.open(gtt["url"])
    elif apod > 0:
        apod = 0
        if "yes" in user_input:            
            output("The explanation of the picture is:\n" + gtt["explanation"])
        elif "no" in user_input:
            output("Okay.")
        else:
            output("Answer with yes or no please")
            apod = 1
    #-------------------------APOD-------------------------#
            

    elif "where a" in user_input or user_input == "wai":
        link = 'https://ipinfo.io/json'
        response = requests.get(link, verify=True)
        result = response.json()
        result = result['region']
        output("Your current location is:\n" + result)
        img = PhotoImage(result + ".png")
        ImgWindow.configure(file=img)
        count = count + 1

    #-------------  Name -------------#
    elif "your name" in user_input:
        global name
        global count_name
        if name != "":
            output("My name is: "+name)
        else:
            output("I dont have a name yet, \n would you want to give me one?")
            count_name = 1
    elif count_name == 1:
        if "yes" in user_input:
            output("Okay, you can write it now.")
            count_name = 2
        elif "no" in user_input:
            output("Okay")
            count_name = 0
        else:
            output("Answer with yes or no please!")
            count_name = 1
    elif count_name == 2:
        name = user_input
        output("Okay, my name is: "+name+" from now." )
        count_name = 0
    #-------------  Name -------------#


    else:
        output("Unknown command \n If you want to see the list of the keywords, you can click on the help button.")

# -------------------------------------------Backend---------------------------------------#
# ------------------------------------------Frontend---------------------------------------#

root = Tk()
root.title("Chat Bot")
root.geometry("600x600")
root.resizable(width=FALSE, height=FALSE)

# ----------------Menu--------------#
main_menu = Menu(root)
main_menu.add_command(label="Help", command=help)
root.config(menu=main_menu)
# ----------------------------------#

chatWindow = Label(root, text=final_output, bd=10, fg="black", font=("Castellar", 20), wraplength=599)
chatWindow.pack()

ImgWindow = PhotoImage(height=400)
Label(root, image=ImgWindow).pack()

raw_input = StringVar()
messageWindow = Entry(root, textvariable=raw_input, bg="#202020", foreground="#3D93E8", font=("Arial", 25))
messageWindow.place(x=5, y=500, height=85, width=440)

Button = Button(root, text="Send", height=5,
                bd=0, bg="#275685", activebackground="#90A9BF", foreground='#ffffff', font=("Arial", 20), command=main)
Button.place(x=450, y=500, height=85, width=143)

root.bind('<Return>', lambda event=None: Button.invoke())
root.attributes('-topmost', True)
root.mainloop()