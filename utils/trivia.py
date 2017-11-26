import urllib2
import json


def gimmie(genre, difficulty, type):
        num = 1
    #    amount = "amount=1&"
    #    category = "category" + "=" + request.form["genre"] + "&"
    #    difficulty = "difficulty" + "=" + request.form["difficulty"] + "&"
    #    Type = "type" + "=" + request.form["type"]
    #    layout = request.form["type"]

        #snippet = amount + category + difficulty + Type
        snippet = 'amount=1&category=22&difficulty=easy&type=multiple'

        u = urllib2.urlopen("https://opentdb.com/api.php?" + snippet)
        data_string = u.read()
        dic = json.loads(data_string)
        questions = []
        answers = []
        incorrect = []
        if dic['response_code'] == 0:
            results = dic["results"]
            for i in range(num):
                questions.append(results[i]["question"])
                answers.append(results[i]["correct_answer"])
                incorrect.append(results[i]['incorrect_answers'])
            print questions + answers + incorrect
        else:
            print "Sorry, we don't have enough of those questions. Try again!"

gimmie(1,1,1)
