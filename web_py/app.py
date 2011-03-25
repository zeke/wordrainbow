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
    '/',            'Index',
)

alnum = map(chr, range(97, 123)) + [str(n) for n in range(0,10)]
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
            return self.mix()
        else:
            return self.initialize_session()
    
    
    def mix(self):
        query_params = web.input(name=None,hex=None,callback="callback")
        colorname    = query_params.name
        colorhex     = query_params.hex
        cb           = query_params.callback
        
        if colorname and colorhex:
            ## we need to post some data to Wordnik, then get tags
            tag = "#" + colorhex.upper()
            tag_word(colorname, tag)
            tags = get_all_tags(colorname)
        else:
            tags = []
        
        return self.choose_new_color(cb, tags)      
    
    def choose_new_color(self, cb, tags):
        l = session.get("colorlist").split(",")
        if not l[0]:
            ## list is empty; reset "playing" cookie and start over
            session.mixing = False
            raise web.seeother('/mix')
        item = l.pop()
        ## reassemble the colorlist cookie with one fewer element
        session.colorlist = ",".join(l)
        
        return "{0}({1})".format(cb, json.dumps( { "nextName": item, "tagsForQuery": get_color_tags(tags) } ))

    def initialize_session(self):
        user_data = web.input()
        colorlist = all_colors.jiggle()
        # colorlist.reverse()
        session.mixing = True
        session.colorlist = ",".join(colorlist)
        raise web.seeother('/mix')



class Identify(object):
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        if session.get("identifying", False):
            return self.identify()
        else:
            return self.initialize_session()
        
    def identify(self):
        query_params = web.input(name=None,hex=None,callback="callback")
        colorname    = query_params.name
        colorhex     = query_params.hex
        cb           = query_params.callback
        
        if colorname and colorhex:
            h = "#" + colorhex.upper()
            wnk.word_get(h, shouldCreate="true")
            tag_word(h, colorname)
            tags = get_all_tags(h)
        else:
            tags = []
        
        return self.choose_new_hex(cb, tags)
        
    def choose_new_hex(self, cb, tags):
        l = session.get("hexen").split(",")
        if not l[0]:
            session.mixing = False
            raise web.seeother('/identify')
        item = l.pop()
        session.hexen = ",".join(l)
        return "{0}({1})".format(cb, json.dumps( { "hexCode": item, "tags": get_color_tags(tags) } ))
        
    def initialize_session(self):
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
            
        
def tag_word(word, tag):
    token = wnk.token
    conn = httplib.HTTPConnection("api.wordnik.com")
    
    headers = { "api_key": KEY, "auth_token": token }
    uuid    = "".join(random.sample(alnum, 4))
    t       = urllib.quote("color:{0}_{1}".format(tag, uuid))
    uri     = "/v4/word.json/{0}/tag?tags={1}&username=wordrainbow".format(urllib.quote(word), t)
    
    conn.request("POST", uri, None, headers)
    r = conn.getresponse()
    
class Visualize(object):
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        query_params = web.input(name=None,hex=None,callback="callback")
        colorname    = query_params.name
        colorhex     = query_params.hex
        cb           = query_params.callback
        
        if colorname:
            tags = get_color_tags(get_all_tags(colorname))
        elif colorhex:
            h = "#" + colorhex.upper()
            tags = get_color_tags(get_all_tags(h))
        else:
            tags = []
        
        return "{0}({1})".format(cb, json.dumps( { "tags": tags } ))
        
        

class Game(object):
    
    name = "game"
    
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")

        if session.get(self.name, False):
            return self.play()
        else:
            return self.initialize_session()


    def play(self):
        colorname, colorhex, cb = self.get_query_params()

        if colorname and colorhex:
            ## we need to post some data to Wordnik, then get tags
            tag_word(colorname, colorhex)
            tags = get_all_tags(colorname)
        else:
            tags = []

        return self.choose_new_color(cb, tags)      

    def choose_new_color(self, cb, tags):
        l = session.get("colorlist").split(",")
        if not l[0]:
            ## list is empty; reset "playing" cookie and start over
            session.mixing = False
            raise web.seeother('/{0}'.format(self.name))
        item = l.pop()
        ## reassemble the colorlist cookie with one fewer element
        session.colorlist = ",".join(l)

        return "{0}({1})".format(cb, json.dumps( { "nextName": item, "tagsForQuery": get_color_tags(tags) } ))

    def initialize_session(self):
        user_data = web.input()
        colorlist = all_colors.jiggle()
        # colorlist.reverse()
        session.mixing = True
        session.colorlist = ",".join(colorlist)
        raise web.seeother('/mix')

    def get_query_params(self):    
        query_params = web.input(name=None,hex=None,callback="callback")
        colorname    = query_params.name
        colorhex     = query_params.hex
        cb           = query_params.callback

        return (colorname, colorhex, cb)

class Index(object):
    def GET(self):
        return render.index()

class count(object):
    def GET(self, name):
        session.count += 1
        return str(session.count)

class reset(object):
    def GET(self, name):
        session.kill()
        return "Resettttted, yo!"

render = web.template.render('templates/')
app     = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})


def get_all_tags(word):
    headers =  { "api_key": KEY }
    tags = wnk._do_http(urllib.quote("/word.json/{0}/tags".format(word)), headers)
    return [ t['name'] for t in json.loads(tags) ]


# main    = app.cgirun()

if __name__ == "__main__":
    app.run()

