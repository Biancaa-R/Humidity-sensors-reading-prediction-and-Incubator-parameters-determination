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

    #Creating the book register table
    cursor.execute("""CREATE TABLE IF NOT EXISTS Register
    (Sp_no INT PRIMARY KEY,
    Book_Title VARCHAR(200) NOT NULL,
    Author_Name VARCHAR(100),
    Publisher VARCHAR(100) NOT NULL,
    Class INT,
    Year_Of_Publication INT,
    Edition VARCHAR(20),
    Subject VARCHAR(50),
    Category VARCHAR(50),
    Cost INT NOT NULL)""")   
    mydb.commit()

    #Creating the book issues table
    cursor.execute("""CREATE TABLE IF NOT EXISTS IssueDetails
    (Sp_no INT,
    Book_Title VARCHAR(200) NOT NULL,
    Author_Name VARCHAR(100),
    Roll_no INT NOT NULL,
    Date_issued DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(50) NOT NULL DEFAULT "Borrowed",
    Due VARCHAR(50))""")
    
    mydb.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS ClientInfo
    (Roll_no INT,
    Name VARCHAR(40),
    Phone BIGINT,
    EmailID VARCHAR(50))""")
    mydb.commit()


