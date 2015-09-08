#! /usr/local/bin/python

# convenience script for starting interactive session
import os
import time
import IPython
from requests_oauthlib import OAuth1Session

os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()

baseRequestURI = 'https://openapi.etsy.com/v2/'

# assigns myshop, client_key, client_secret, oauth_token, and oauth_token_secret
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

def actuallyFindAllShopTransactions(shop):
    oset = 0
    limit = 100
    response = findAllShopTransactions(shop, limit, oset).json()
    total = response['count']
    oset += 100
    finaldata = []
    finaldata += response['results']
    while (oset < total):
        response = findAllShopTransactions(shop,limit, oset).json()
        finaldata += response['results']
        oset += 100
    return finaldata

IPython.embed()
