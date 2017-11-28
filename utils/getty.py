import urllib2
import json

the_key = open('static/.apikey', 'r').read().replace('\n','')

def test():
    # This is a test url
    url = "https://api.gettyimages.com/v3/search/images?fields=id,title,thumb,referral_destinations&sort_order=best&phrase=hello"

    # Necessary to access info from API, must be used like this EVERY time
    opener = urllib2.build_opener()
    opener.addheaders = [('Api-Key', the_key)]
    json = opener.open(url)
    json = json.read()

    #print json
    print len(json)

def list_urls(phrase):
    url = "https://api.gettyimages.com/v3/search/images?fields=id,title,thumb,referral_destinations&sort_order=best&phrase=" + phrase
    print url
    opener = urllib2.build_opener()
    opener.addheaders = [('Api-Key', the_key)]
    try:
        response = opener.open(url)
        json_string = response.read()
        dictionary = json.loads(json_string)
        list_of_urls = [""]
        if dictionary["result_count"] > 0:
            for image in dictionary["images"]:
                list_of_urls.append(image["display_sizes"][0]["uri"])
        return list_of_urls
    except:
        print "error"
        return [""]

def search(phrase):
    #prepositions and articles
    fillers = "the a an about above across after against along alongside amid among are around as at before behind below between but by did do does down during featured features following for from got had has have how in inside into is less like long longest many more much near never no not of off on onto opposite out outside over short shortest since than through to toward towards under underneath unlike until up upon versus via was were what when which why within without you".split(" ")
    #so that every word has a space in front of it
    phrase = " " + phrase.lower() + " "
    #get rid of punctuation
    phrase = phrase.replace(",", "").replace("?", "").replace(".", "").replace("'", "").replace('"', "")
    #get rid of all fillers
    for word in fillers:
        phrase = phrase.replace(" "+word+" ", " ")
    #get rid of extra whitespace
    phrase = phrase.strip()
    #limit phrase
    phrase = "+".join(phrase.split(" ")[:3])
    return list_urls(phrase)
