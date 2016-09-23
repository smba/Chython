# -*- coding: iso-8859-1 -*-
from praefixe import praefix
from atome import atomlist
from copy import deepcopy
from PSE import namen,name
from Benutzeroberflaeche import *
from Benutzeroberflaeche import Chiralitaetszentrenordner
import string
global metalle
praefix['aquo']='["O",["H",[0,1,0]],["H",[0,1,0]]]'
praefix['amonio']='["N",["H",[0,1,0]],["H",[0,1,0]],["H",[0,1,0]]]'
praefix['carbonyl']='["C",[0,1,0],["O",[0,3,0]]]'
praefix['nitrosyl']='["N",[0,1,0],["O",[0,3,0]]]'
metalle={"ferrat":"Fe","niccolat":"Ni","cuprat":"Cu","molybdat":"Mo","argentat":"Ag","aurat":"Au","mercurat":"Hg","stannat":"Sn","plumbat":"Pb"}
#lateinische Sondernamen von Metallen
class Praefix_K:
    def __init__(self,Name,Lokant=1,Bezeichnungen=[],Bindungen=[1],Id=1,sicherzugeordnete=[]):
        if type(Name)==list:
            self.Beschreibung=Name[1:]
            self.Name=Name[0]
        else:
            if Name not in praefix:
                Name=Name[:-1]
            self.Beschreibung=eval(praefix[Name])
            self.Name=Name
        self.Lokant=Lokant
        self.Bindungen=Bindungen
        self.Bezeichnungen=Bezeichnungen
        self.Untergruppen=unterGruppen(sicherzugeordnete)
        self.parent=False
        self.id=Id
    def AtominBeschreibung(self,parameter):
        if str(parameter) in self.Beschreibung:
            return True
    def unterordnen(self,gruppe=[]):
        if type(gruppe)==list:
            for i in gruppe:
                self.Untergruppen.unterordnen(i)
        else:
            self.Untergruppen.unterordnen(gruppe)
    def adoptieren(self,parent):
        self.parent=parent
    def sucheVEP(self,speziell=True):
        a=deepcopy(self.Beschreibung)
        if a[1][0].__class__!=str:
            return a
        a=sucheVEP(a,speziell)[0]
        a.insert(1,[0,1,0])
        return Chiralitaetszentrenordner(a)
class Komplex():
    #Zentralatom       =  ZA
    #Ladung ZA         =  LZA
    #Strukturpraefixe  =  SP
    #Substituenten     =  S
    #Kationen          =  K
    def __init__(self,ZA,LZA,SP,S,K):
        self.ZA=ZA
        self.LZA=LZA
        self.SP=SP
        self.S=S
        self.K=K
    def inSP(self,x):
        if x in self.SP:
            return True
    def Info(self):
        print "--------"
        print "Zentralatom        :",x.ZA
        print "Ladung Zentralatom :",x.LZA
        print "Strukturpraefixe   :",x.SP
        print "Kationen           :",x.K
        print "Substituenten      :"
        for i in x.S:
            print "                   - ",i.sucheVEP()
        print "--------"
    def Bauen(self):
        syntax=[]
        for i in self.S:
            syntax.append(i.sucheVEP())
        #Behandlung von Stereoisomeren bei Oktaedergestalt
        if self.inSP("fac") or self.inSP("mer"):
            for i in syntax:
                if syntax.count(i)==3:
                    for i2 in range(3):
                        syntax.remove(i)
                    if self.inSP("fac"):
                        syntax=[i,i,i]+syntax
                    else:
                        syntax=[i,i]+syntax+[i]
                    break
        if self.inSP("cis") or self.inSP("trans"):
            for i in syntax:
                if syntax.count(i)==2:
                    for i2 in range(2):
                        syntax.remove(i)
                    if self.inSP("cis"):
                        syntax=[i,i]+syntax
                    else:
                        syntax=[i]+syntax+[i]
                    break
        syntax=[self.ZA]+syntax
        return syntax
        #aus den gegebenen Parametern wird der Bauplan erstellt

def sucheVEP(x,speziell):
    #sucht in der Beschreibung eines zukuenftigen Liganden nach einem schoenen
    #Valenzelektronenpaar für eine koordinative Bindung,
    #im Zweifelsfall einfach speziell
    for i in range(1,len(x)):
        if x[i][0].__class__!=str:
            continue
        if "@" in x[i][0]:
            continue
        if eval("symbol"+x[i][0]).ordnungszahl>4:
            #guck mal, ein schoenes Valenzelektronenpaar
            x[i][0]+="*"
            return x,True
        x[i],a=sucheVEP(x[i],speziell)
        if a:
            return x,True
    return x,False
def Komplexanalyse(a):
    #Analysiert den Namen eines Komplexes
    a=string.lower(a)
    komplex=[0,0,[],[]]
    kationen=[]
    while a!="":
        a,S_griechischeswort=sfgw_K(a)
        a,S_isomerie=sonderz_K(a)
        a,S_praefix=praes_K(a)
        a,S_zentral=zentral_K(a)
        if S_isomerie:
            komplex[2].append(S_isomerie)
        if S_praefix:
            S_praefix=deepcopy(Praefix_K(S_praefix))
            if S_griechischeswort:
                for i in range(S_griechischeswort):
                    komplex[3].append(S_praefix)
            else:
                komplex[3].append(S_praefix)
        if S_zentral:
            if komplex[0]:
                kationen.append(komplex[0])
            if S_zentral in metalle:
                komplex[0]=metalle[S_zentral]
            else:
                if S_zentral.endswith("at"):
                    S_zentral=S_zentral[:-2]
                komplex[0]=name[S_zentral.capitalize()]
            a,komplex[1]=sfrw_K(a)
        if not S_praefix and not S_praefix and not S_zentral:
            a=a[1:]
    return Komplex(komplex[0],komplex[1],komplex[2],komplex[3],kationen)
def sfgw_K(a):
    num = ["mono","di","tri","tetra","penta","hexa","hepta","octa","nona","deca","undeca","dodeca","trideca","tetradeca","pentadeca","hexadeca","heptadeca","octadeca","nonadeca","eicosa"]
    for i in num:
        if a.startswith(i):
            return a[len(i):],num.index(i)+1
    return a,0
def sonderz_K(a):
    print a
    for i in ["cis","trans","fac","mer"]:
        if a.startswith(i):
            print i
            return a[len(i):],i
    return a,[]
def praes_K(x):
    p=praefix.keys()
    p.sort()
    p.reverse()
    #praefixe werden so geordnet, das groessere vorne stehen, "sulfono" vor "sulfo"
    for a in p:
        if a[-1]!="o" and not a.endswith("yl"):
            a2=a+"o"
        else:
            a2=a
        if x.startswith(a2):
            return x[len(a2):],a2
    return x,False
def zentral_K(a):
    global metalle
    for i in metalle:
        if a.startswith(i):
            return a[len(i):],i
    for i in namen:
        i2=string.lower(i)
        i3=i2.replace("ium","")+"at"
        if a.startswith(i3):
            #anionischer Komplex
            return a[len(i3):],i3
        if a.startswith(i2):
            return a[len(i2):],i2
            #neutraler Komplex
    return a,""
def sfrw_K(x):
    if not x.startswith("("):
        return x,0
    x=x[1:]
    rl=["i","ii","iii","iv","v","vi","vii","viii"]
    for i in rl:
        if x.startswith(i+")"):
            return x[len(i)+1:],rl.index(i)+1
    return x,0
#Test
print Komplexanalyse("trans-difluorotetrachloroplatinat(IV)").Bauen()