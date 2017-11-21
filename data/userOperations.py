import sqlite3   #enable control of an sqlite database
import hashlib   #allows for passwords to be encrypted

f = "dingbubble.db"

def openDB():
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitate db ops
    return db, c

def closeDB(db):
    db.commit()
    db.close()

def createTable():
    db, c = openDB()
    command = "CREATE TABLE Users(username TEXT PRIMARY KEY, password TEXT, highscores TEXT)"
    c.execute(command)
    closeDB(db)

def getHighscores(username): #user
    # returns user's highscores formatted as a dictionary
    db, c = openDB()
    command = "SELECT highscores FROM Users WHERE username = '%s'" % (username)
    for i in c.execute(command):
        highscore = i[0]
    closeDB(db)
    return highscore

def addHighscore(username, subject, score): #user, subject, score
    db, c = openDB()
    command = ""
    c.execute(command)
    closeDB(db)

def getUser(username):
    db, c = openDB()
    command = "SELECT username FROM Users WHERE username = %s" % (username)
    closeDB(db)

def authUser(username, password): #user, password
    # assuming password is already passed in encrypted form
    db, c = openDB()
    command = "SELECT * FROM Users where username = %s AND password = %s" % (username, password)
    closeDB(db)
    return c.execute(command)[0]

def addUser(username, password): #user, password
    db, c = openDB()
    command = "INSERT INTO Users VALUES(%s, %s, '')" % (username, password)
    c.execute(command)
    closeDB(db)

#createTable()
print getHighscores('beep')
