import random

class uberList(list):
    def jiggle(self, strength=5):
        done = 0
        l = []
        while len(l) < len(self):
            slice = self[done:done+strength]
            l.extend(random.sample(slice, len(slice)))
            done += strength
        return uberList(l)