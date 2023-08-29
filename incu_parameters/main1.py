import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QWidget,QMainWindow,QPushButton
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
import dbdetails,db
import mysql.connector
import requests, json
import sklearn
import warnings
from requests.exceptions import ConnectionError

from datetime import datetime
import time
import telepot
import serial
            

from telepot.loop import MessageLoop
warnings.filterwarnings('ignore')

incuhum=0
incutemp=0
resp_rate=0
volume=0

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

#y=predictions.execute(age,weight,heatout,roomhum,roomtemp)
#print(y)
#self.value.setText("incubator_humidity to be set :",incuhum, "incubator_temperature to be set :",incutemp,"respiratory rate of the child per minute: ",resp_rate,"respiratory air volume in ml of the child",volume)
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




def custom_excepthook(type, value, traceback):
    # Handle exceptions and warnings here
    # You can display a message or log the issue
    print("Exception or warning occurred:", type, value)

# Install the custom excepthook
sys.excepthook = custom_excepthook

def show_warning():
    warnings.warn("This is a sample warning!")



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
        self.register2.clicked.connect(self.gototable)

    def gototable(self):
        table=TableScreen()
        widget.addWidget(table)
        widget.setCurrentIndex(widget.currentIndex()+1)

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


class TeleScreen(QDialog):
    def __init__(self):
        super(TeleScreen,self).__init__()
        loadUi("choo.ui",self)
        self.ok.clicked.connect(self.gotosendmsg)
        self.cancel.clicked.connect(self.gotocancel)
        self.dash.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotowelcome)

    def gotosendmsg(self):
        print("The bot is started")
        from telepot.loop import MessageLoop

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

        bot = telepot.Bot('api key of bot')

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




    def gotocancel(self):
        self.value.setText("The bot is terminated")
        print("bot stopped")

        

    def gotowelcome(self):
        welcome=WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotodash(self):
        dash=DashScreen()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)




class PredScreen(QDialog):
    def __init__(self):
        super(PredScreen,self).__init__()
        loadUi("addpat.ui",self)

        self.predict.clicked.connect(self.gotoresult1)
        self.logout.clicked.connect(self.gotowelcome)
        self.dash.clicked.connect(self.gotodash)

    def gotoresult1(self):
        global age,weight,heatout,roomtemp,roomhum
        global incuhum,incutemp,resp_rate,volume
        age=int(self.age1.text())
        weight=int(self.weight1.text())
        heatout=float(self.heatout1.text())
        roomtemp=float(self.temp.text())
        roomhum=float(self.hum.text())

        self.age1.setText("")
        self.weight1.setText("")
        self.heatout1.setText("")
        self.temp.setText("")
        self.hum.setText("")

        '''try:
            # Enter your API key here
            api_key = "cb107b2a951040dd7226208a5d508799"

            # base_url variable to store url
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city_name="Chennai"
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
                pass
                print(" City Not Found ")

        except:
            ConnectionError'''
        '''
        #y=predictions.execute(age,weight,heatout,roomhum,roomtemp)
        #print(y)
        #self.value.setText("incubator_humidity to be set :",incuhum, "incubator_temperature to be set :",incutemp,"respiratory rate of the child per minute: ",resp_rate,"respiratory air volume in ml of the child",volume)
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
        '''


        
        from sklearn.linear_model import LinearRegression
        linear=LinearRegression()
        
        linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]].values,dataset1[["incutemp"]].values)
        linear.feature_names_in_=["age","weight","heatout","roomhum","roomtemp"]
        y=np.array([[age,weight,heatout,roomhum,roomtemp]])
        
        prediction=linear.predict(y)
        #["age","weight","heatout","roomhum","roomtemp"]
        incutemp=(float(prediction))
        
        #linear=LinearRegression()
        linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]].values,dataset1[["incuhum"]].values)
        linear.feature_names_in_=["age","weight","heatout","roomhum","roomtemp"]
        y=np.array([[age,weight,heatout,roomhum,roomtemp]])
        prediction=linear.predict(y)
        incuhum=(float(prediction))

        linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]].values,breath[["resp_rate"]].values)
        linear.feature_names_in_=["age","weight","heatout","roomhum","roomtemp"]
        y=np.array([[age,weight,heatout,roomhum,roomtemp]])
        prediction=linear.predict(y)
        resp_rate=(float(prediction))

        linear.fit(dataset1[["age","weight","heatout","roomhum","roomtemp"]].values,breath[["volume"]].values)
        linear.feature_names_in_=["age","weight","heatout","roomhum","roomtemp"]
        y=np.array([[age,weight,heatout,roomhum,roomtemp]])
        prediction=linear.predict(y)
        volume=(float(prediction))

        print("incubator_humidity to be set",incuhum)
        print("incubator_temperature to be set",incutemp)
        print("respiratory rate of the child per minute",resp_rate)
        print("respiratory air volume in ml of the child",volume)

        #requests.get('https://api.thingspeak.com/update?api_key=B5HXLPLMWO3DQE1O&field1='+str(temperature)+'&field2='+str(humidity)+'&field3='+str(incutemp)+'&field4='+str(incuhum)+'&field5='+str(resp_rate)+'&field6='+str(volume))
        import serial
        import time

        ser=serial.Serial("COM5",9600,timeout=1)

        time.sleep(2)
        list1=[]
        for i in range(0,2):
            line=ser.readline()
            line=line.decode("utf")
            #print(line)
    
            if line not in ["DHTxx test!",""]:
                y=line.split()
                if len(y)>3 :
                    humidity=y[1]
                    temperature=y[3]
                    time.sleep(10)
                    if humidity in ["test","test!"]:
                        continue

                        
                    import requests
                    import time
        

                    requests.get('https://api.thingspeak.com/update?api_key=B5HXLPLMWO3DQE1O&field1='+str(temperature)+'&field2='+str(humidity)+'&field3='+str(incutemp)+'&field4='+str(incuhum)+'&field5='+str(resp_rate)+'&field6='+str(volume))


        self.data1.setText("  incuhum "+str(round(incuhum,2)))
        self.data2.setText("  incutemp "+str(round(incutemp,2)))
        self.data3.setText("  resp_rate "+str(round(resp_rate,2)))
        self.data4.setText("  volume "+str(round(volume,2)))
        self.value.setText("value added to the cloud successfully")
        #Each time I add this,it should goto the cloud



    def gotowelcome(self):
        welcome=WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotodash(self):
        dash=DashScreen()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)

class TableScreen(QDialog):
    def __init__(self):
        super(TableScreen,self).__init__()
        loadUi("table.ui",self)
        self.loaddata()
        self.dash.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotowelcome)

    def loaddata(self):
        
        r=requests.get('https://api.thingspeak.com/channels/2246600/feeds.json?api_key=JJ9LVBW5OZR47G87')
        n=json.loads(r.text)
        '''for i in range(len(n['feeds'])):
            list1=[n["feeds"][i]["entry_id"],n['feeds'][i]['field1'],n['feeds'][i]['field2'],n['feeds'][i]['field3'],n['feeds'][i]['field4'],n['feeds'][i]['field5'],n["feeds"][i]["field6"],n['feeds'][i]['created_at']]
            #i is the row count
            y=enumerate(list1)
            for j in y:
                self.registertable.setItem(i,j[0],QtWidgets.QTableWidgetItem(j[1]))'''
        self.registertable.setRowCount(len(n["feeds"]))
        for i in range(len(n["feeds"])):
            list1=[n["feeds"][i]["entry_id"],n['feeds'][i]['field1'],n['feeds'][i]['field2'],n['feeds'][i]['field3'],n['feeds'][i]['field4'],n['feeds'][i]['field5'],n["feeds"][i]["field6"],n['feeds'][i]['created_at']]
            #i is the row count
            
            self.registertable.setItem(i,0,QtWidgets.QTableWidgetItem(str(list1[1])))
            self.registertable.setItem(i,1,QtWidgets.QTableWidgetItem(str(list1[2])))
            self.registertable.setItem(i,2,QtWidgets.QTableWidgetItem(str(list1[3])))
            self.registertable.setItem(i,3,QtWidgets.QTableWidgetItem(str(list1[4])))
            self.registertable.setItem(i,4,QtWidgets.QTableWidgetItem(str(list1[5])))
            self.registertable.setItem(i,5,QtWidgets.QTableWidgetItem(str(list1[6])))
            self.registertable.setItem(i,6,QtWidgets.QTableWidgetItem(str(list1[7])))
            self.registertable.setColumnWidth(6,500)
            self.registertable.setColumnWidth(4,200)
            self.registertable.setColumnWidth(5,200)

        
    

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
