from datetime import datetime
import telepot

from telepot.loop import MessageLoop

incuhum=0
incutemp=0
resp_rate=0
volume=0

def th():
    import serial
    import time

    ser=serial.Serial("COM5",9600,timeout=1)

    time.sleep(0.5)
    list1=[]

    for i in range(0,5):
        line=ser.readline()

        line=line.decode("utf")
        #print(line)       

        if line not in ["DHTxx test!",None]:
            y=line.split()
            if len(y)>3 :
                humidity=y[1]
                temperature=y[3]
                if humidity in ["test","test!"]:
                    continue
                if len(humidity)>0:
                    list1.append(humidity)
                    list1.append(temperature)
                
                return (list1)
                    #time.sleep(10)

                    #requests.get('https://api.thingspeak.com/update?api_key=B5HXLPLMWO3DQE1O&field1='+str(temperature)+'&field2='+str(humidity)+'&field3='+str(incutemp)+'&field4='+str(incuhum)+'&field5='+str(resp_rate)+'&field6='+str(volume)


                    #humidity = round(humidity, 2)
                    #temperature = round(temperature, 2)

bot = telepot.Bot('6355723537:AAHCm412-9KGQFhM6xoO0C1D-DXsLMLvdYc')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #if you want to allow access only from a certain user enable the below line and use intentaion for the rest of the LOCs untill MessageLoop, To get your telegram ID use underinfobot
    #if(msg['from']['id']==*):
    if('username' in msg['from']):
        print(msg['from']['username'], " Sent msg",msg['text']," ")
    else:
        print(msg['text'])
    if(msg['text'] == '/dht'):
        r=th()
        
            
        bot.sendMessage(chat_id, " current Temp of incubator: "+str(r[0]))


        bot.sendMessage(chat_id, "current Humdidity of incubator: "+str(r[1]))
        bot.sendMessage(chat_id, "Temperature of incubator to be set"+str(incutemp))
        bot.sendMessage(chat_id, "humidity of incubator to be set"+str(incuhum)) 

    if(msg['text'] == '/rates'):
        r=th()
        bot.sendMessage(chat_id, " current Temp of incubator: "+str(r[0]))
        bot.sendMessage(chat_id, "current Humdidity of incubator: "+str(r[1]))
        bot.sendMessage(chat_id, "breath rate of the child per minute: "+ str(resp_rate))

    if (msg['text'].lower() in ["thanks","thank you","thankyou"] ):
        bot.sendMessage(chat_id,"welcome ")
        

MessageLoop(bot, handle).run_as_thread()

