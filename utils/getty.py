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

def search(phrase):
    url = "https://api.gettyimages.com/v3/search/images?fields=id,title,thumb,referral_destinations&sort_order=best&phrase=" + phrase
    opener = urllib2.build_opener()
    opener.addheaders = [('Api-Key', the_key)]
    response = opener.open(url)
    json_string = response.read()
    dictionary = json.loads(json_string)
    list_of_urls = []
    if dictionary["result_count"] > 0:
        for image in dictionary["images"]:
            list_of_urls.append(image["display_sizes"][0]["uri"])
    return list_of_urls
