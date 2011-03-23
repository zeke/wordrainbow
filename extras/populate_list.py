#!/usr/bin/env python

import httplib, json, random, sys

from wordnik import Wordnik

w = Wordnik(api_key="d92d8109432f0ead8000707303d0c6849e23be119a18df853",
            username="wordrainbow", password="gomer")

def add_word(word):
    token = w.token
    key = w._api_key
    headers = { "api_key": key, "auth_token": token,
                'Content-Type': 'application/json' }

    conn = httplib.HTTPConnection("api.wordnik.com")
    
    uri = "/v4/wordList.json/wordrainbow/words?username=wordrainbow"
    body = json.dumps([
                       {
                        "word": word,
                       }
                      ])
    
    print body
    conn.request("POST", uri, body, headers)
    r = conn.getresponse()
    return r.status, r.reason

try:
    f = open(sys.argv[1])
except:
    print "give me a file"
    sys.exit(1)

for color in f:
    color = color.strip()
    print add_word(color)

