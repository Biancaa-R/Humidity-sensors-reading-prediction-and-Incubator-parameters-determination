from datetime import datetime
import time
import serial
import time

ser=serial.Serial("COM5",9600,timeout=1)

time.sleep(0.5)

while True:
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
            print(humidity,temperature)
            #time.sleep(10)


