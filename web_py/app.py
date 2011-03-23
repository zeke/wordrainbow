#!/usr/bin/env python

import web, playmode, json, random
from wordnik import Wordnik
from helpers import uberList

web.config.debug = False

urls = (
    '/mix',         'Mix',
    '/identify',    'Identify',
    '/visualize',   'Visualize',
    '/',            'Index',
)



app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
w = Wordnik(api_key="1d3baf57f57254b5c430200e729037e9dea9d87493f3a16b4",username="wordrainbow",password="gomer")
all_colors = uberList([ w['word'] for w in json.loads(w.word_list_get_words("wordrainbow")) ])


class Identify(object):
    def GET(self):
        if session.get("playing", False):
            print "stuff already set"
            l = session.get("colorlist").split(",")
            if not l[0]:
                ## list is empty; reset "playing" cookie and start over
                session.playing = False
                raise web.seeother('/identify')
            item = l.pop()
            session.colorlist = ",".join(l)
            return json.dumps( { "color": item } )
        else:
            user_data = web.input()
            colorlist = all_colors.jiggle()
            colorlist.reverse()
            session.playing = True
            session.colorlist = ",".join(colorlist)
            raise web.seeother('/identify')

class Mix(object):
    hexen = ["0", "3", "6", "9", "C", "F"]
    def GET(self):
        user_data = web.input()
        return json.dumps({ "colorCode": "".join(random.sample(self.hexen, 3)) } )
        
class Visualize(object):
    def GET(self):
        user_data = web.input()

class Index(object):
    def GET(self):
        return "Index.Htm"

class count(object):
    def GET(self, name):
        session.count += 1
        return str(session.count)

class reset(object):
    def GET(self, name):
        session.kill()
        return "Resettttted, yo!"



if __name__ == "__main__":
    app.run()

