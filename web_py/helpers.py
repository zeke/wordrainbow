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
    
def get_color_tags(l):
    tags = []
    for item in l:
        if item.startswith("color:"):
            s = re.sub("_.*", "", item).replace("color:", "")
            tags.append(s.replace("#", ""))
    return tags
    