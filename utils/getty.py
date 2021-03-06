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

#returns a list of urls to images using the supplied phrase; /static/mystery.png by default
def list_urls(phrase):
    url = "https://api.gettyimages.com/v3/search/images?fields=id,title,comp,referral_destinations&sort_order=best&phrase=" + phrase
    print url
    #sizes are thumb, preview, comp, high_res_comp and display_set (for all sizes)
    opener = urllib2.build_opener()
    opener.addheaders = [('Api-Key', the_key)]
    try:
        response = opener.open(url)
        json_string = response.read()
        dictionary = json.loads(json_string)
        list_of_urls = []
        if dictionary["result_count"] > 0:
            for image in dictionary["images"]:
                list_of_urls.append(image["display_sizes"][0]["uri"])
        return list_of_urls + ["/static/mystery.png"]
    except:
        print "error"
        return ["/static/mystery.png"]

def search(phrase):
    #prepositions and articles
    fillers = "the a an about above acronym across after against along alongside amid among are around as at before behind below between but by call called calls derisive did do does down during featured features following for from got had has have how if in inside into is known less like long longest many more much name named names near never no not of off on onto opposite out outside over short shortest since than that these this those through to toward towards under underneath unlike until up upon versus via was were what when which why within without you".split(" ")
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
