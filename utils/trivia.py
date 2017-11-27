import urllib2
import json


def gimmie(genre, difficulty, Type):
        num = 1
        amount = "amount=1&"
        category = "category" + "=" + genre + "&"
        difficulty = "difficulty" + "=" + difficulty + "&"
        Type1 = "type" + "=" + Type
        layout = Type

        snippet = amount + category + difficulty + Type1
        #snippet = 'amount=1&category=22&difficulty=easy&type=multiple'

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
            return [questions[0], answers[0]] + incorrect[0]
        else:
            return []
