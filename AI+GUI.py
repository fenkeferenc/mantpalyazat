from tkinter import *
from datetime import datetime
import requests
import wikipedia
import webbrowser
import json
from ttkthemes import ThemedTk
import os
from random import randint

#---------------------------------Backend---------------------------------#
w_api_key = "76ce09d339c3310433855fceee368b9d"
final_output = ""
count = 0
apod = 0
gtt = ""
#--------------------------------#
def enter(event=None):
    ()
#--------------------------------#
def weatherimg():
    global ImgWindow
    global count
    os.chdir(os.path.dirname(__file__))
    r = str(randint(1,3))
    img = PhotoImage(weather_description + r + ".png")
    ImgWindow.configure(file=img)
    count = count + 1
    
def output(x):
    global final_output
    final_output = x
    print(final_output)
    global chatWindow
    chatWindow.configure(text=final_output)
    messageWindow.delete(0,"end")
def main():
    global count
    global ImgWindow
    user_input = str(raw_input.get()).lower()
    
    if count > 0:
        count = 0
        ImgWindow.blank()

    if "exit" in user_input.lower():
        output("[+] Program stopped")
        input("Press enter to exit")
        exit()

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
        output("The current date is:"+ current_time)

    elif "weather" in user_input.lower():
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = "Kourou"
        complete_url = base_url + "appid=" + w_api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]

            current_temperature = y["temp"]
            #----------------------------------------#
            celsius = current_temperature -272,15 
            #----------------------------------------#
            z = x["weather"]
            global weather_description
            weather_description = z[0]["description"]

            output(" The current temperature in "+city_name+" is: " + str(celsius).replace('(', '')[:3] +"C degree(s)"
                  "\n The weather in " +city_name +" is: "+
                            str(weather_description))

            if "rain" in weather_description:
                weather_description = "rain"
                weatherimg()

            elif "cloud" in weather_description:
                weather_description = "clouds"
                weatherimg()
            else:
                pass

        else:
            output(" City Not Found ")
        
    elif "search" in user_input.lower():
        try:
            lowcase = str(user_input.lower())
            data = lowcase.replace("search ", "")
            print("Searching for: " + data)
            new = data.translate({ord(i): None for i in ' '})
            output(wikipedia.summary(new, sentences=5))
        except:
            output("Wikipedia page was not found")


    elif "lang" in user_input.lower():
        try:
            a = input("Enter search language: ")
            wikipedia.set_lang(a)
            print("language succesfully set to "+ a)
        except:
            print("Wrong input")

    elif "picture of the day" in user_input or user_input == "apod":
        global apod
        global gtt
        apod = 1
        print("set apod to 1")
        f = r"https://api.nasa.gov/planetary/apod?api_key=XMqdRJg4lgeRUm0N1ETvfUvymjgmfhXJ7ot2Udgj"
        data = requests.get(f)
        gtt = json.loads(data.text)
        output("The astronomy picture of the day is: \n" + gtt["title"] + "\n Do you want to hear the explanation of this picture?")
        webbrowser.open(gtt["url"])

    elif apod > 0:
        apod = 0
        if user_input == "yes":
            output("The explanation of the picture is:\n" + gtt["explanation"])
        elif user_input == "no":
            output("Okay.")
        else:
            output("Answer with yes or no please")
            return

    elif "your name" in user_input:
        output("I dont have a name yet:(")

    elif "help" in user_input.lower():
        output("Keyword list: \n time \n date \n weather \n search")
    else:
        output("asd")
#-------------------------------------------Backend---------------------------------------#
#------------------------------------------Frontend---------------------------------------#

root = ThemedTk(theme="arc")
root.title("Chat Bot")
root.geometry("500x600")
root.resizable(width=FALSE, height=FALSE)

#----------------Menu--------------#
main_menu = Menu(root)

file_menu = Menu(root)

main_menu.add_command(label="Quit", command=exit)
root.config(menu=main_menu)
#----------------------------------#

chatWindow = Label(root, text=final_output, bd = 10, fg = "black", font = "Castellar", wraplength=500)
chatWindow.pack()

ImgWindow = PhotoImage(height=220)
Label(root, image=ImgWindow).pack()

raw_input = StringVar()
messageWindow = Entry(root, textvariable=raw_input, bg="black", foreground="#00ffff", font=("Arial", 25))
messageWindow.place(x=128, y=500, height=88)

Button= Button(root, text="Send",  width="12", height=5,
                    bd=0, bg="#0080ff", activebackground="#00bfff",foreground='#ffffff',font=("Arial", 12), command=main)
Button.place(x=6, y=500, height=88)


root.bind('<Return>', lambda event=None: Button.invoke())
root.attributes('-topmost', True)
root.mainloop()
