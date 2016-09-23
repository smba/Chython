from visual import *
from Ausfuehren import *
import random
class bindung(cylinder):
    def __init__(self,anfang,ende):
        self=cylinder(pos=anfang,axis=ende-anfang)
    def drehe(self,zentrum,winkel,achse):
        self.pos=rotate(self.pos-zentrum,winkel,achse)+zentrum
        self.axis=rotate(self.pos-zentrum,winkel,achse)+zentrum
        self.naechste.drehe(zenrum,winkel,achse)
    def naechstebindung(self,naechste):
        self.naechste=naechste
def verbinde(x):
    a=bindung(vector(0,0,0),norm(vector(random.random(),random.random(),random.random())))
    bindungen=[a]
    for i in range(x):
        a=norm(vector(random.random(),random.random(),random.random()))
        b=bindung(bindungen[-1].pos,bindungen[-1].pos+a)
        bindungen.append(b)
        bindungen[-2].naechstebindung(bindungen[-1])
verbinde(5)
