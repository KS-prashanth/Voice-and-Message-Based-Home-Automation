from cProfile import run
import re
from subprocess import call


import speech_recognition as sr
import serial
import RPi.GPIO as GPIO
import os, time
import  vlc
import requests, json
from datetime import datetime
import telegram
import sys
import yfinance as yf
import pyjokes
import wikipedia
import requests
import random


r = sr.Recognizer()
led = 18
text = {}
text1 = {}
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
now = datetime.now()

api_key = '5420542013:AAGOqyu15UDX97SHysvjOswSZbnw5hAtISA'
user_id = '943695428'

bot = telegram.Bot(token=api_key)


def ping():
    p = vlc.MediaPlayer("/home/pi/ping.mp3")
    p.play()

def listen1():
    with sr.Microphone(device_index=2) as source:
        r.adjust_for_ambient_noise(source)
        print("Say Something")
        ping()
        audio = r.listen(source)
        print("got it")
    return audio


def voice(audio1):
    try:
        text1 = r.recognize_google(audio1)
        print("you said: " + text1)
        return text1
    except sr.UnknownValueError:
        call(["espeak", "-s140  -ven+18 -z", "I could not understand, please repeat"])
        print("I could not understand, please repeat")
        return 0
    except sr.RequestError as e:
        print("Could not request results from Google")
        return 0


def music():
    p = vlc.MediaPlayer("/home/pi/1.mp3")
    p.play()
    time.sleep(10)
    p.stop()

def todaynews(): 
    url = "http://newsapi.org/v2/top-headlines?country=in&apiKey=59ff055b7c754a10a1f8afb4583ef1ab"
    page = requests.get(url).json() 
    article = page["articles"] 
    results = [] 
    for ar in article: 
        results.append(ar["title"])
    newsNumber = random.randint(0,len(results)-1)
    return results[newsNumber]
    



def weather():

    api_key = "3b22805c1d2bb37b60e868e0380d83ef"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Coimbatore"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    current_temperature = []
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"] - 273.15
        current_temperature = round(current_temperature,2)
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]

        z = x["weather"]
        weather_description = z[0]["description"]
    else:
        print(" City Not Found ")

    return current_temperature,current_humidity,current_pressure,weather_description


def main(text):
    text = text.lower()
    if "light on" in text or "lights on" in text:
        GPIO.output(led, 1)
        call(["espeak", "-s140  -ven+18 -z", "okay  Sir, Switching ON the Lights"])
        print("Lights on")
        bot.send_message(chat_id=user_id, text='Light is switch ON in bedroom')
        
    elif "light off" in text or "lights off" in text:
        GPIO.output(led, 0)
        call(["espeak", "-s140  -ven+18 -z", "okay  Sir, Switching off the Lights"])
        print("Lights Off")
        bot.send_message(chat_id=user_id, text='Light is switch OFF in bedroom')
        
    elif "hello" in text:
        call(
            ["espeak", "-s140  -ven+18 -z", "Hi TEAM-11 How can i be at your service!"]
        )
    elif "who are you" in text:
        call(
            ["espeak", "-s140  -ven+18 -z", "I am a voice assistant built by team 11"]
        )
    elif "your birthday" in text:
        call(
            ["espeak", "-s140  -ven+18 -z", "I was built on july 13"]
        )

    elif "message" in text:
        messageTo = text.replace('message',"")
        
        if "dad" in messageTo:
            messageInfo = messageTo.replace('dad',"")
            
            bot.send_message(chat_id= '1188356245', text= messageInfo)
            call([
                "espeak",
                "-s140  -ven+18 -z",
                "Message sent to dad",
            ])
        
        if "mom" in messageTo or "mum" in messageTo:
            messageInfo = messageTo.replace('mom',"")
            messageInfo = messageTo.replace('mum',"")
            
            bot.send_message(chat_id= '974159522', text= messageInfo)
            call([
                "espeak",
                "-s140  -ven+18 -z",
                "Message sent to mom",
            ])   

        else:
            call(
                [
                "espeak",
                "-s140  -ven+18 -z",
                "I didn't understand, please give a valid command",
                ]
                )


    elif "how are you" in text:
        call(
            ["espeak", "-s140  -ven+18 -z", "I am exited to serve you "]
        )
    elif "where are you" in text:
        call(
            ["espeak", "-s140  -ven+18 -z", "I am in the cen department of amrita school of engneering coimbatore "]
        )
    elif "your nationality" in text or "your country" in text:
        call(
            ["espeak", "-s140  -ven+18 -z", "I am made in India , jai hind "]
        )
    elif "thank you" in text or "nice" in text:
        call(
            ["espeak", "-s140  -ven+18 -z", " Happy to help you       have a nice day  "]
        )
    elif "what is the time" in text or "time" in text:
        call(
            [
                "espeak",
                "-s140  -ven+18 -z",
                "The Time is : " + now.strftime("%I:%M  %p"),
            ]
        )
    elif "what day" in text:
        call([
                "espeak",
                "-s140  -ven+18 -z",
                "Today is : " + now.strftime("%A"),
            ])
    elif "What is the temperature " in text or "temperature" in text:
         current_temperature,current_humidity,current_pressure,weather_description=weather()
         call(
            [
                "espeak",
                "-s140  -ven+18 -z",
                "The Temperature is : " +str(current_temperature)+"degree celcius"
            ]
        )
         
    elif "weather outside " in text or "weather" in text:
         weather_description=weather()
         call(
            [
                "espeak",
                "-s140  -ven+18 -z",
                "The weather outside is : " +str(weather_description[3])
            ]
        )
         
    elif "send the schedule " in text:
        if now.strftime("%A").lower == "monday":
         call([
                "espeak",
                "-s140  -ven+18 -z",
                "sending you the schedule for  : "+ now.strftime("%A"),
            ])
         shed = "8:40am - 10:20am : IBS \n10:20am - 12:10pm : MIS \n12:10pm - 1:00pm : AVP \n2:50pm - 4:30pm : ICN"
        
        elif now.strftime("%A").lower == "tuesday":
         call([
                "espeak",
                "-s140  -ven+18 -z",
                "sending you the schedule for  : "+ now.strftime("%A"),
            ])
         shed = "8:40am - 10:20am : ICN \n10:20am - 12:10pm : ROS \n12:10pm - 1:00pm : MIS \n2:50pm - 4:30pm : DAA"
        
        elif now.strftime("%A").lower == "saturday":
         call([
                "espeak",
                "-s140  -ven+18 -z",
                "sending you the schedule for  : "+ now.strftime("%A"),
            ])
         shed = "8:40am - 10:20am : MIS \n10:20am - 12:10pm : ICN \n12:10pm - 1:00pm : BDA \n2:50pm - 4:30pm : DAA"
        
             
        else:
         call([
                "espeak",
                "-s140  -ven+18 -z",
                "sending you the schedule for  : "+ now.strftime("%A"),
            ])
         shed = "today is free we you can sleep"
                    
        bot.send_message(chat_id=user_id, text= shed)   
    
        
    elif "music" in text:
         call([
                "espeak",
                "-s140  -ven+18 -z",
                "playing the music",
            ])
         music()
         
    elif "tell me a joke" in text:
        
        v = pyjokes.get_joke()
        
        call([
                "espeak",
                "-s140  -ven+18 -z",
                "Ok let me think a joke ; " +str(v),
            ])
         
    elif "quit" in text or "exit" in text:
         call([
                "espeak",
                "-s140  -ven+18 -z",
                "OK nice talking to you I'm going to sleep mode",
            ])
         sys.exit()
    elif "my stocks" in text:
        
        apple = yf.Ticker("aapl")
        appleDict = dict(apple.info)
        appleValue = appleDict["currentPrice"]
        appleRecom = appleDict["recommendationKey"]

        google = yf.Ticker("GOOGL")
        googleDict = dict(google.info)
        googleValue = googleDict["currentPrice"]
        googleRecom = googleDict["recommendationKey"]
        
        valueText =  "The stock prices in your portfolio is : \n-> Apple : " +str(appleValue)+ " USD \n   Recommendation : " +str(appleRecom)+ "\n-> Google : " +str(googleValue)+ " USD \n   Recommendation : " +str(googleRecom)

        bot.send_message(chat_id=user_id, text= valueText)
        
        call(
            [
                "espeak",
                "-s140  -ven+18 -z",
                "The stock price of Apple is : " +str(appleValue)+ "USD" + " ; and google is : " +str(googleValue)+ "USD"
            ])
    
    elif 'news' in text:
        newsVar = todaynews()
        call([
            "espeak",
            "-s140  -ven+18 -z",
            "let me search for today's news ; " +str(newsVar)
        ])    
    

    elif 'who is' in text:
        query = text.replace('who is',"")
        wi = wikipedia.summary(query,2)
        call([
                "espeak",
                "-s140  -ven+18 -z",
                 str(wi),
            ])


if __name__ == "__main__":
    while 1:
        audio1 = listen1()
        text = voice(audio1)
        if text is 0:
            time.sleep(2)
            continue
        main(text)
        time.sleep(2)
           



