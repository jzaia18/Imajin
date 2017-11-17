import sqlite3   #enable control of an sqlite database
import hashlib   #allows for passwords to be encrypted

def createTables():
    f="data/dingbubble.db"

    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor() #facilitate db ops

    command - ""
    c.execute(command)
    
    db.commit()
    db.close()

def getHighscores(): #user
    # returns user's highscores formatted as a dictionary
    #return eval()

def addHighscore(): #user, subject
    pass

def findUser(): #user, password
    pass

def addUser(): #user, password
    pass
