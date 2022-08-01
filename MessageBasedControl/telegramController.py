import time
import telepot
from telepot.loop import MessageLoop
import RPi.GPIO as GPIO
from datetime import datetime
import os
import sys
import subprocess

bulb = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(bulb, GPIO.OUT)
GPIO.output(bulb, 0)
now = datetime.now()

lightsOnOff = 0

def action(msg):
    chat_id = msg['chat']['id']
    commandIrregular = msg['text']
    command = commandIrregular.lower()
    print('Request received...processing...')
    
    global lightsOnOff
    
    if 'hey' in command or 'holla' in command:
        message = "Hey Team11!! \nWhat can i do for you? \n => To turn on/off lights: \n turn on/off lights  \n => To know ligths are on/off: \nis lights on/off \n => To get pic of the room: \nsituation update"
        
    elif 'turn on lights' in command:
        message = "Lights are switched on"
        GPIO.output(bulb, 1)
        lightsOnOff = 1

    elif 'turn off lights' in command:
        message = "Lights are switched off"
        GPIO.output(bulb, 0)
        lightsOnOff = 0
    
    elif 'is lights on or off' in command or 'is lights on' in command or 'is lights off' in command:
        if lightsOnOff == 1:
            message = "Lights are ON"
        if lightsOnOff == 0:
            message = "Lights are OFF"

    elif 'situation update' in command:
        
        currentdate = now.strftime("%Y-%m-%d_%H-%M")
        script_dir = os.path.dirname(__file__)
        os.system('./webcam.sh')
        
        rel_path = currentdate +".jpg"
        abs_file_path = os.path.join(script_dir, rel_path)

        imageLocation = '/home/pi/webCam/' + rel_path
        message = 'Pic taken on ' + now.strftime("%b %d %Y, %I:%M %p")
        telegram_bot.sendPhoto(chat_id, photo=open(imageLocation, 'rb'))
        print("Image taken")
        
        mydir='/home/pi/webCam'

        for file in os.listdir(mydir):
            if file.endswith('.jpg'):
                os.remove(os.path.join(mydir,file))     
    
    else:
        message = "Invalid command!!"
                  
    telegram_bot.sendMessage(chat_id, message)

telegram_bot = telepot.Bot('5487181544:AAH3jOg0Ru7s6dIwleWfZDaW41zTHnRHwRw')
MessageLoop(telegram_bot, action).run_as_thread()
while 1:
    time.sleep(10)
print('Send the command to turn on or off the light...')