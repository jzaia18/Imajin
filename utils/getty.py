import urllib2
import json

the_key = open('../.apikey', 'r').read().replace('\n','')

# This is a test url
url = "https://api.gettyimages.com/v3/search/images?fields=id,title,thumb,referral_destinations&sort_order=best&phrase=hello"

# Necessary to access info from API, must be used like this EVERY time
opener = urllib2.build_opener()
opener.addheaders = [('Api-Key', the_key)]
json = opener.open(url)
json = json.read()

print json
