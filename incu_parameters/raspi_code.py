import numpy as np
import pandas as pd
import shutup
#shutup.please()
dataset1=pd.read_csv("refined.csv")
x=dataset1[["age","weight","heatout","roomhum","roomtemp"]].copy()
y=dataset1[["incuhum"]].copy()
x["intercept"]=1
x=x[["intercept","age","weight","heatout","roomhum","roomtemp"]]
x_t=x.T
B=np.linalg.inv(x_t@x)@x_t@y


B.index=x.columns
predictionsh=x@B


x=dataset1[["age","weight","heatout","roomhum","roomtemp"]].copy()
y=dataset1[["incutemp"]].copy()
x["intercept"]=1
x=x[["intercept","age","weight","heatout","roomhum","roomtemp"]]
x_t=x.T
B=np.linalg.inv(x_t@x)@x_t@y


B.index=x.columns
predictionst=x@B

prediction=pd.concat([dataset1["incuhum"],predictionsh["incuhum"],dataset1["incutemp"],predictionst["incutemp"]],axis=1)
prediction.columns=["actual_incuhum","predicted_incuhum","actual_incutemp","predicted_incutemp"]

#Part 2:

breath=pd.read_csv("breath.csv")
x=breath[["age","weight","heatout","roomhum","roomtemp"]].copy()
y=breath[["resp_rate"]].copy()
x["intercept"]=1
x=x[["intercept","age","weight","heatout","roomhum","roomtemp"]]
x_t=x.T
B=np.linalg.inv(x_t@x)@x_t@y

B.index=x.columns
predictionsr=x@B

x=breath[["age","weight","heatout","roomhum","roomtemp"]].copy()
y=breath[["volume"]].copy()
x["intercept"]=1
x=x[["intercept","age","weight","heatout","roomhum","roomtemp"]]
x_t=x.T
B=np.linalg.inv(x_t@x)@x_t@y

B.index=x.columns
predictionsv=x@B

prediction_final=pd.concat([breath["resp_rate"],predictionsr["resp_rate"],breath["volume"],predictionsv["volume"]],axis=1)
prediction_final.columns=["resp_rate_actual","resp_rate_prediction","volume_actual","volume_predicted"]

#SAMPLE DATA
from sklearn.linear_model import LinearRegression
linear=LinearRegression()

age=int(input("Enter the gestational age of the infant completed in weeks"))
weight=int(input("Enter the weight of the infant in grams"))
heatout=float(input("Enter the heat emitted out of the incubator"))


import requests, json

# Enter your API key here
api_key = "cb107b2a951040dd7226208a5d508799"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = input("Enter city name : ")

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x = response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":

	# store the value of "main"
	# key in variable y
	y = x["main"]

	# store the value corresponding
	# to the "temp" key of y
	current_temperature = y["temp"]

	# store the value corresponding
	# to the "pressure" key of y
	current_pressure = y["pressure"]

	# store the value corresponding
	# to the "humidity" key of y
	current_humidity = y["humidity"]

	# store the value of "weather"
	# key in variable z
	z = x["weather"]

	# store the value corresponding
	# to the "description" key at
	# the 0th index of z
	weather_description = z[0]["description"]

	# print following values
	print(" Temperature (in kelvin unit) = " + str(current_temperature) + "\n atmospheric pressure (in hPa unit) = " +
	      str(current_pressure) + "\n humidity (in percentage) = " + str(current_humidity) + "\n description = " + str(weather_description))
	roomtemp=current_temperature-273.16
	roomhum=current_humidity

	


else:
	print(" City Not Found ")
	roomtemp=float(input("Enter the temprature of the room"))
	roomhum=float(input("Enter the humidity of the room"))


linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]].values,dataset1[["incutemp"]].values)
y=np.array([[age,weight,heatout,roomhum,roomtemp]])
prediction=linear.predict(y)
#["age","weight","heatout","roomhum","roomtemp"]
incutemp=(float(prediction))

#linear=LinearRegression()
linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]].values,dataset1[["incuhum"]].values)
y=np.array([[age,weight,heatout,roomhum,roomtemp]])
prediction=linear.predict(y)
incuhum=(float(prediction))

linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]].values,breath[["resp_rate"]].values)
y=np.array([[age,weight,heatout,roomhum,roomtemp]])
prediction=linear.predict(y)
resp_rate=(float(prediction))

linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]].values,breath[["volume"]].values)
y=np.array([[age,weight,heatout,roomhum,roomtemp]])
prediction=linear.predict(y)
volume=(float(prediction))

print("incubator_humidity to be set",incuhum)
print("incubator_temperature to be set",incutemp)
print("respiratory rate of the child per minute",resp_rate)
print("respiratory air volume in ml of the child",volume)

import requests
import time
import Adafruit_DHT as dht
while True:
    humidity,temperature=dht.read_retry(dht.DHT11,4)
    requests.get('https://api.thingspeak.com/update?api_key=B5HXLPLMWO3DQE1O&field1='+str(temperature)+'&field2='+str(humidity)+'&field3='+str(incutemp)+'&field4='+str(incuhum)+'&field5='+str(resp_rate)+'&field6='+str(volume))
    break

from datetime import datetime
import time
import telepot
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from telepot.loop import MessageLoop
#Connect DHT11 to pin 4

GPIO.setmode(GPIO.BCM)

def th():
    humidity,temperature = dht.read_retry(dht.DHT11, 4)
    humidity = round(humidity, 2)
    temperature = round(temperature, 2)
    return temperature,humidity

bot = telepot.Bot('6355723537:AAHCm412-9KGQFhM6xoO0C1D-DXsLMLvdYc')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #if you want to allow access only from a certain user enable the below line and use intentaion for the rest of the LOCs untill MessageLoop, To get your telegram ID use underinfobot
    #if(msg['from']['id']==************):
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
        bot.sendMessage(chat_id, " current Temp of incubator: "+str(r[0]))
        bot.sendMessage(chat_id, "current Humdidity of incubator: "+str(r[1]))
        bot.sendMessage(chat_id, "breath rate of the child per minute: "+ str(resp_rate))  


MessageLoop(bot, handle).run_as_thread()
