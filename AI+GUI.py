from tkinter import *
from datetime import date, datetime
import requests
import wikipedia
import webbrowser
import json

#---------------------------------Backend---------------------------------#
w_api_key = "76ce09d339c3310433855fceee368b9d"
final_output = ""
#--------------------------------#
def enter(event=None):
    ()
#--------------------------------#

def output(x):
    global final_output
    final_output = x
    print(final_output)
    global chatWindow
    chatWindow.configure(text=final_output)
    messageWindow.delete(0,"end")
    
    

def main():

    user_input = str(raw_input.get()).lower()

    if "exit" in user_input.lower():
        output("[+] Program stopped")
        input("Press enter to exit")
        exit()

    if "time" in user_input.lower():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        output("The current time is:" + current_time)
        if "date" in user_input.lower():
            now = datetime.now()
            current_time = now.strftime("%D")
            output("And the current date is:" + current_time)
            

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

            weather_description = z[0]["description"]

            output(" The current temperature in "+city_name+" is: " + str(celsius).replace('(', '')[:3] +"C degree(s)"
                  "\n The weather in " +city_name +" is: "+
                            str(weather_description))

        else:
            output(" City Not Found ")
        
    elif "search" in user_input.lower():
        try:
            lowcase = str(user_input.lower())
            print("Searching for: " + lowcase)
            data = lowcase.replace("search", "")
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

    elif "picture of the day" in user_input:
        f = r"https://api.nasa.gov/planetary/apod?api_key=XMqdRJg4lgeRUm0N1ETvfUvymjgmfhXJ7ot2Udgj"
        data = requests.get(f)
        tt = json.loads(data.text)
        output("The picture of the day according to NASA is: \n" + tt["title"])
        webbrowser.open(tt["url"])

    elif "your name" in user_input:
        output("I dont have a name yet:(")

    elif "help" in user_input.lower():
        output("Keyword list: \n time \n date \n weather \n search")
    else:
        output("asd")
#-------------------------------------------Backend---------------------------------------#
#------------------------------------------Frontend---------------------------------------#

root = Tk()
root.title("Chat Bot")
root.geometry("500x600")
root.resizable(width=FALSE, height=FALSE)

#----------------Menu--------------#
main_menu = Menu(root)

file_menu = Menu(root)

main_menu.add_command(label="Quit", command=exit)
root.config(menu=main_menu)
#----------------------------------#

chatWindow = Label(root, text=final_output, bd = 100, fg = "black", font = "Castellar", wraplength=500)
chatWindow.pack()

def worker():
    print(str(raw_input.get()))
    

raw_input = StringVar()
messageWindow = Entry(root, textvariable=raw_input, bg="black", foreground="#00ffff", font=("Arial", 25))
messageWindow.place(x=128, y=500, height=88)

Button= Button(root, text="Send",  width="12", height=5,
                    bd=0, bg="#0080ff", activebackground="#00bfff",foreground='#ffffff',font=("Arial", 12), command=main)
Button.place(x=6, y=500, height=88)


root.bind('<Return>', lambda event=None: Button.invoke())

root.mainloop()
