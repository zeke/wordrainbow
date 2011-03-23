import json, random, re

class uberList(list):
    def jiggle(self, strength=5):
        done = 0
        l = []
        while len(l) < len(self):
            slice = self[done:done+strength]
            l.extend(random.sample(slice, len(slice)))
            done += strength
        return uberList(l)

def create_hexen():
    hexen = ["0", "3", "6", "9", "C", "F"]
    hexlist = []
    for r in hexen:
        for g in hexen:
            for b in hexen:
                hexlist.append("#{0}{1}{2}".format(r,g,b))
    random.shuffle(hexlist)
    return hexlist
    
def get_color_tags(s):
    try:
        j = json.loads(s)
        tags = []
        for item in j:
            if item['name'].startswith("color:#"):
                tags.append(re.sub("_.*", "", item['name']).replace("color:", ""))
        return tags
    except:
        return []
