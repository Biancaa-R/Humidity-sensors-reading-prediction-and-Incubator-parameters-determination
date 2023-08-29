#-----------------------------------------------
#Connecting to server and creating new database
#-----------------------------------------------

import mysql.connector

def exec(dbuser, dbpass):
    #Connecting to server
    mydb = mysql.connector.connect(
                host = "localhost",
                user = dbuser,            
                password = dbpass,
                database="library"
            )

    cursor = mydb.cursor()
    
    #Creating database
    cursor.execute("CREATE DATABASE IF NOT EXISTS library")
    cursor.execute("USE library")

    #Creating login table
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_info
    (name VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL PRIMARY KEY,
    password VARCHAR(30) NOT NULL)""")
    mydb.commit()

    
