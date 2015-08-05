#! /usr/local/bin/python

from requests_oauthlib import OAuth1Session

baseRequestURI = 'https://openapi.etsy.com/v2/'

with open('../resources/EtsyAPI.ck', 'r') as f:
    exec(f.read(), globals())

oauth = OAuth1Session(client_key, client_secret=client_secret,\
        resource_owner_key=oauth_token, resource_owner_secret=oauth_token_secret)

def findAllShopTransactions(shop, limit=25, offset=0):
    request_URI = baseRequestURI + """shops/%s/transactions?limit=%s&offset=%s""" % (shop, str(limit), str(offset))
    return oauth.get(request_URI) 

def findAllShopReceipts(shop, limit=25, offset=0, was_shipped=None):
    request_URI = baseRequestURI
    if was_shipped is not None:
        request_URI += """shops/%s/receipts?limit=%s&offset=%swas_shipped=%s"""\
                % (shop, str(limit), str(offset), str(was_shipped).lower())
    else:
        request_URI += """shops/%s/receipts?limit=%s&offset=%s"""\
                % (shop, str(limit), str(offset))
    return oauth.get(request_URI)

total = 4049
oset = 0
finaldata = []
while (oset < total):
    response = findAllShopTransactions('caresspress', 100, oset)
    jsondata = response.json()
    finaldata += jsondata['results']
    oset += 100
oset = 0
x = findAllShopReceipts('caresspress')
