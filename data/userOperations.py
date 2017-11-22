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
        highscores = i[0]
    closeDB(db)
    return eval(highscores)

def addHighscore(username, subject, score): #user, subject, score
    db, c = openDB()
    highscores = getHighscores(username)
    print True
    print highscores
    highscores[subject] = score
    print "also true"
    print repr(highscores)
    command = "UPDATE users SET '%s'" % (repr(highscores))
    c.execute(command)
    closeDB(db)

def getUser(username):
    db, c = openDB()
    command = "SELECT username FROM Users WHERE username = '%s'" % (username)
    closeDB(db)

def authUser(username, password): #user, password
    # assuming password is already passed in encrypted form
    db, c = openDB()
    command = "SELECT * FROM Users where username = '%s' AND password = '%s'" % (username, password)
    userList = c.execute(command)
    for user in  userList:
        print user
    closeDB(db)
    return 'end of authUser'
    # return username in 

def addUser(username, password): #user, password
    db, c = openDB()
    command = "INSERT INTO Users VALUES('%s', '%s', '{}')" % (username, password)
    c.execute(command)
    closeDB(db)

if __name__ == "__main__":
    db, c = openDB()
    c.execute("CREATE TABLE Users(username TEXT PRIMARY KEY, password TEXT, highscores TEXT)")
    closeDB(db)
    addUser('beep', 123)
    addHighscore('beep', 'math', 10)
    print getHighscores('beep')
    #print addUser('boop', 'abc')
    #addHighscore('boop', 'history', 2)
    #print authUser('beep', 123)
   # addHighscore('beep', 'boop', 999) 
