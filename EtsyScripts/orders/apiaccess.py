#! /usr/local/bin/python

from requests_oauthlib import OAuth1Session

baseRequestURI = 'https://openapi.etsy.com/v2/'

with open('../resources/EtsyAPI.ck', 'r') as f:
    exec f.read() in globals()

oauth = OAuth1Session(client_key, client_secret=client_secret,\
        resource_owner_key=oauth_token, resource_owner_secret=oauth_token_secret)

def findAllShopTransactions(shop, limit=25, offset=0):
    request_URI = baseRequestURI + """shops/%s/transactions?limit=%s&offset=%s""" % (shop, str(limit), str(offset))
    return oauth.get(request_URI) 


finaldata = []
#x = findAllShopTransactions("caresspress", 100)
#data = x.json()
#finaldata += data['results']

total = 4049
oset = 0
while oset < total:
    x = findAllShopTransactions('caresspress', 100, oset)
    data = x.json()
    finaldata += data['results']
    oset += 100

f = open('testout.txt', 'w')
for item in finaldata:
    f.write(str(item['variations']) + '\n')

f.close()
