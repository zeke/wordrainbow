#!/usr/bin/env python

import web
import hashlib, httplib, json, random, time, urllib
from wordnik import Wordnik
from helpers import *

web.config.debug = False

urls = (
    '/mix',         'Mix',
    '/identify',    'Identify',
    '/visualize',   'Visualize',
    '/play',        'Play',
    '/(.*)',        'Index',
)


KEY="d92d8109432f0ead8000707303d0c6849e23be119a18df853"
# w = Wordnik(api_key="1d3baf57f57254b5c430200e729037e9dea9d87493f3a16b4",username="wordrainbow",password="gomer")
## privileged key!
wnk = Wordnik(api_key=KEY,username="wordrainbow",password="gomer")
all_colors = uberList([ w['word'] for w in json.loads(wnk.word_list_get_words("wordrainbow")) ])
hexen = create_hexen()

class Mix(object):
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        if session.get("mixing", False):
            tags = []
            
            query_params = web.input(name=None,hex=None,callback="callback")
            cb = query_params.callback
            if query_params.name and query_params.hex:
                tag_word(query_params.name, query_params.hex)
                headers =  { "api_key": KEY }
                tags = wnk._do_http(urllib.quote("/word.json/{0}/tags".format(query_params.name)), headers)
            
            l = session.get("colorlist").split(",")
            if not l[0]:
                ## list is empty; reset "playing" cookie and start over
                session.mixing = False
                raise web.seeother('/mix')
            item = l.pop()
            session.colorlist = ",".join(l)
            
            return "{0}({1})".format(cb, json.dumps( { "nextName": item, "tagsForQuery": get_color_tags(tags) } ))
        else:
            user_data = web.input()
            colorlist = all_colors.jiggle()
            # colorlist.reverse()
            session.mixing = True
            session.colorlist = ",".join(colorlist)
            raise web.seeother('/mix')

class Identify(object):
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        tags = []
        query_params = web.input(name=None,hex=None,callback="callback")
        cb = query_params.callback
        if query_params.name and query_params.hex:
            wnk.word_get(query_params.hex, shouldCreate="true")
            headers =  { "api_key": KEY }
            tags = wnk._do_http(urllib.quote("/word.json/{0}/tags".format(query_params.hex)), headers)
            tags = [ t['name'] for t in json.loads(tags) ]
        if session.get("identifying", False):
            l = session.get("hexen").split(",")
            if not l[0]:
                session.mixing = False
                raise web.seeother('/identify')
            item = l.pop()
            session.hexen = ",".join(l)
            return "{0}({1})".format(cb, json.dumps( { "hexCode": item, "tags": tags } ))
        else:
            session.identifying = True
            l = hexen
            random.shuffle(l)
            try:
                l.remove("#000")
                l.remove("#FFF")
            except:
                pass
            session.hexen = ",".join(l)
            session.identifying = True
            raise web.seeother('/identify')
            
        
def tag_word(word, code):
    token = wnk.token
    conn = httplib.HTTPConnection("api.wordnik.com")
    
    headers = { "api_key": KEY, "auth_token": token }
    uuid = hashlib.md5(time.time().__str__()).hexdigest()
    uri = "/v4/word.json/{0}/tag?".format(word)
    tag = urllib.quote("color:#{0}_{1}".format(code, uuid))
    uri += "tags={0}&username=wordrainbow".format(tag,uuid)
    
    conn.request("POST", uri, None, headers)
    r = conn.getresponse()
    
class Visualize(object):
    def GET(self):
        user_data = web.input()

class Index(object):
    def GET(self, f):
        if not f:
            f = "index.html"
        try:
            return open(f).read()
        except:
            return "Sorry, can't find that page"
class count(object):
    def GET(self, name):
        session.count += 1
        return str(session.count)

class reset(object):
    def GET(self, name):
        session.kill()
        return "Resettttted, yo!"

app     = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})

# main    = app.cgirun()

if __name__ == "__main__":
    app.run()

