import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QWidget
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
import dbdetails,db
import mysql.connector

#creating database and new table in mysql 
dbuser, dbpass = dbdetails.execute()
db.exec(dbuser,dbpass)

#Connecting to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = dbuser,            
    password = dbpass,
    database = "library"
    )
         
cursor = mydb.cursor()
cursor = mydb.cursor(buffered=True)

import numpy as np
import pandas as pd
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


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen,self).__init__()
        loadUi("welcomescreen.ui",self)
        self.username.setPlaceholderText("Username")
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.sign.clicked.connect(self.gotosignup)
        self.login.clicked.connect(self.gotodash)

    def gotosignup(self):
        signup=SignupScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotodash(self):
        global username
        username = self.username.text()
        password = self.passw.text()

        if len(username)==0 or len(password)==0:
            self.error.setText("Please fill in all fields")
        
        else:
            query = "SELECT password FROM login_info WHERE username = '"+username+"'"
            cursor.execute(query)    
            result_pass = cursor.fetchone()

            if result_pass is not None:
                if result_pass[0] == password:
                    print("Successfully logged in.")
                    dash=DashScreen()
                    widget.addWidget(dash)
                    widget.setCurrentIndex(widget.currentIndex()+1)


                else:
                    self.error.setText("Invalid username or password")
            else:
                self.error.setText("Invalid username or password")
class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen,self).__init__()
        loadUi("signup.ui",self)
        self.signupname.setPlaceholderText("Enter your name")
        self.signupuser.setPlaceholderText("Enter your user name")
        self.signuppass.setPlaceholderText("Enter your password")
        self.confirmpass.setPlaceholderText("confirm your password")

        self.signuppass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

        self.signup2.clicked.connect(self.gotosignup)
        self.backtologin.clicked.connect(self.gotowelcome)

        #self.signup1.setText("user added successfully, please login")

    def gotosignup(self):
        global newname, newuser, newpass
        newname = self.signupname.text()
        newuser = self.signupuser.text()
        newpass1 = self.signuppass.text()
        newpass2 = self.confirmpass.text()

        if len(newname)== 0 or len(newuser) == 0 or len(newpass1) == 0 or len(newpass2) == 0:
            self.signup1.setText("Please fill in all fields")

        elif newpass1 != newpass2:
            self.signup1.setText("The passwords do not match")

        else:
            cursor.execute("SELECT * FROM login_info WHERE username = '"+newuser+"'")
            data = cursor.fetchall()
            if data:
                self.signuperror.setText("Username already exists")
            else:
                addnewquery = "INSERT IGNORE INTO login_info VALUES\
                    ('"+newname+"','"+newuser+"','"+newpass1+"')"
                cursor.execute(addnewquery)
                mydb.commit()
                self.signup1.setText("Added new user to database. Successful! please login")

    def gotowelcome(self):
        welcome=WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

class DashScreen(QDialog):
    def __init__(self):
        super(DashScreen,self).__init__()
        loadUi("dashboard.ui",self)
        cursor.execute("SELECT name FROM login_info WHERE username = '"+username+"'")
        greetname = cursor.fetchone()[0]
        self.name.setText("Hello "+greetname+"!")

        self.logout.clicked.connect(self.gotowelcome)
        self.new2.clicked.connect(self.gotopred)
        self.tele.clicked.connect(self.gototele)

    def gotowelcome(self):
        welcome=WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotopred(self):
        pred=PredScreen()
        widget.addWidget(pred)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gototele(self):
        #You have to be in the tele screen for connecting in telegram with doc
        tele=TeleScreen()
        widget.addWidget(tele)
        widget.setCurrentIndex(widget.currentIndex()+1)
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

class PredScreen(QDialog):
    def __init__(self):
        super(PredScreen,self).__init__()
        loadUi("addpat.ui",self)

        self.predict.clicked.connect(self.gotoresult)
        self.logout.clicked.connect(self.gotowelcome)
        self.dash.clicked.connect(self.gotodash)

    def gotoresult(self):
        age=self.age.text()
        weight=self.weight.text()
        heatout=self.heatout/text()

        from sklearn.linear_model import LinearRegression
        linear=LinearRegression()

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


        linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]],dataset1[["incutemp"]])
        y=np.array([[age,weight,heatout,roomhum,roomtemp]])
        prediction=linear.predict(y)
        #["age","weight","heatout","roomhum","roomtemp"]
        incutemp=(float(prediction))

        #linear=LinearRegression()
        linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]],dataset1[["incuhum"]])
        y=np.array([[age,weight,heatout,roomhum,roomtemp]])
        prediction=linear.predict(y)
        incuhum=(float(prediction))

        linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]],breath[["resp_rate"]])
        y=np.array([[age,weight,heatout,roomhum,roomtemp]])
        prediction=linear.predict(y)
        resp_rate=(float(prediction))

        linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]],breath[["volume"]])
        y=np.array([[age,weight,heatout,roomhum,roomtemp]])
        prediction=linear.predict(y)
        volume=(float(prediction))

        print("incubator_humidity to be set",incuhum)
        print("incubator_temperature to be set",incutemp)
        print("respiratory rate of the child per minute",resp_rate)
        print("respiratory air volume in ml of the child",volume)

        self.value.setText("incubator_humidity to be set :",incuhum, "incubator_temperature to be set :",incutemp,"respiratory rate of the child per minute: ",resp_rate,"respiratory air volume in ml of the child",volume)

    def gotowelcome(self):
        welcome=WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotodash(self):
        dash=DashScreen()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
app=QApplication(sys.argv)
welcome=WelcomeScreen()
widget=QStackedWidget()
widget.addWidget(welcome)
#widget.setFixedHeight(800)
#widget.setFixedWidth(1200)
widget.resize(1400, 750)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exitting")
