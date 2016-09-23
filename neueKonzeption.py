# -*- coding: iso-8859-1 -*-
import webbrowser
import wx
from wx.lib.agw import fourwaysplitter,flatnotebook
import ImageGrab # from PIL
import os
import array
import string
import copy as oldcopy
import visual
from os import getcwd,system
from math import *
from visual import pi,cos,sin,sphere,cylinder,cone,curve,cross,rotate,vector,display,arcsin,diff_angle,norm,mag,absolute,arange,frame,label,proj
from win32gui import *
from win32con import *
from atome import atomlist
from praefixe import praefix
from suffixe import suffix
from string import capitalize,upper,letters,lower,digits,split
from PSE import namen,name
from wx.lib.wordwrap import wordwrap
import csv
from os import getcwd
wx.SetDefaultPyEncoding("iso-8859-1")
#Hier wurde gerade zur Sicherheit alles importiert

#Neue Analyse, objektorientierte Herangehensweise:
#Folgende Veraenderungen sollen gegenüber der Vorversion
#zur erheblichen Vereinfachung beitragen:

#Analyse
#Die Analyse laeuft in ihrem Prinzip mit den verwendetetn Modulen weiter,
#wird jedoch dahingehend veraendert, dass die Array-Struktur der Informationen
#ueber gefundene Namensbestandteile in eine objektorientierte Strukttur umgewandelt wird

#Analyseordnung
#Entscheidene Aenderungen sollen vor allem in diesem Bereich durchgefuehrt werden.
#Zu den neuen Aufgaben gehoert unter anderem eine systematischere Zuordnung der
#Einzelelemente, die durch die objektorientierte Herangehensweise vereinfacht werden soll

#Beschreibungserstellung und Umsetzung
#Auch hier soll langfristig eine voellig neue Methode verwandt werden, bei der PARALLEL zur
#Beschreibungserstellung der Zeichenprozess beginnt. Diese Methode soll Heransgehensweisen wie
#die sich erst aus der raeumlichen bzw. zweidimensionalen Struktur hervorgehende Lokantengebung
#bei polycyclischen Systemen vereinfachen. Eine Beschreibung wird trotzdem erstellt, um nachtraegliche
#Arbeiten wie die Ordnung an Chiralitatszentren durchfuehren zu koennen. Die einzelnen Elemente werden
#schließlich nach der berechneten Ordnung zusammengesetzt.
class System:
    def __init__(self,Laenge,Endungen={},Bezeichnungen=[],sicherzugeordnete=[],Radikal=False,Lokant=1,aromatisch=False):
        self.Laenge=Laenge
        self.Endungen=Endungen
        self.Bezeichnungen=Bezeichnungen
        self.Radikal=Radikal
        self.Untergruppen=sicherzugeordnete
        self.Lokant=Lokant
        self.aromatisch=aromatisch
        self.parent=False
    def isRadikal(self):
        if self.Radikal:
            return True
    def unterordnen(self,gruppe):
        if type(gruppe)==list:
            for i in gruppe:
                self.Untergruppen.append(i)
        else:
            self.Untergruppen.append(gruppe)
    def inEndungen(self,parameter):
        for i in self.Endungen:
            if parameter in self.Endungen[i]:
                return i
    def inBezeichnungen(self,parameter):
        if parameter in self.Bezeichnungen:
            return True
    def adoptieren(self,parent):
        self.parent=parent
class Praefix:
    def __init__(self,Name,Lokant=1,Bezeichnungen=[],Bindungen=[1],sicherzugeordnete=[]):
        if type(Name)==list:
            self.Beschreibung=Name[1:]
            self.Name=Name[0]
        else:
            self.Beschreibung=eval(praefix[Name])
            self.Name=Name
        self.Lokant=Lokant
        self.Bindungen=Bindungen
        self.Bezeichnungen=Bezeichnungen
        self.Untergruppen=sicherzugeordnete
        self.parent=False
    def AtominBeschreibung(self,parameter):
        if str(parameter) in self.Beschreibung:
            return True
    def unterordnen(self,gruppe):
        if type(gruppe)==list:
            for i in gruppe:
                self.Untergruppen.append(i)
        else:
            self.Untergruppen.append(gruppe)
    def adoptieren(self,parent):
        self.parent=parent
class Suffix:
    def __init__(self,Name,Lokant=1,Bezeichnungen=[],sichereBindungen=[1],sicherzugeordnete=[]):
        self.Beschreibung=eval(suffix[Name])
        self.Name=Name
        self.Lokant=Lokant
        self.Bezeichnungen=Bezeichnungen
        self.Bindungen=sichereBindungen
        self.Untergruppen=sicherzugeordnete
        self.parent=False
    def AtominBeschreibung(self,parameter):
        if str(parameter) in self.Beschreibung:
            return True
    def unterordnen(self,gruppe):
        if type(gruppe)==list:
            for i in gruppe:
                self.Untergruppen.append(i)
        else:
            self.Untergruppen.append(gruppe)
    def adoptieren(self,parent):
        self.parent=parent
    def praefixconvert(self):
        self=Praefix([self.Name]+self.Beschreibung,self.Lokant,self.Bindungen,self.Untergruppen)

#Hier endet die Klassengesellschaft
def analyse(x):
    #mit objektorientierter Ausgabe
    global csubs,snl,zuckerpraefixe,greek1,cyc,greek2,snl,mi,praelist,fuell,fehlerapp,cyc2
    cyc2=0
    snl=[]
    praelist=[]
    fuell=[]
    cyc=0
    #x=zu analysierender Name
    ausgabe=[]
    #Ausgabe der Analysefunktion in der Art
    #[ Anzahl Kohlenstoffatome , Endungen , Signalworte , Substituenten]
    coefi = []
    #temporÃ¤re Koeffizienten
    gw = []
    #griechische Zahlworte
    praefixe = []
    #speichert alle aktuellen praefixe
    endsilben = []
    #speichert alle aktuellen suffixe
    trivials = []
    #speichert alle aktuellen sonderworte
    trivials2={}
    #speichert noch zu verteilenden sonderworte
    #(sonderworte denen noch ein substituent bzw. eine stammgruppe zugewiesen werden muss)
    trivialsend=[]
    #speichert sonderworte, die erst für die stammgruppe gelten, z. B. "(e)"
    verlauf=[]
    #Speicherung der gefundendenen Silben in chronologischer Reihenfolge
    for i in name.values():
        if i+"-" in x:
            x=x.replace(i+"-",lower(i)+"*-")
            snl.append(lower(i)+"*-")
        if i+"," in x:
            i2=x.index(i+",")
            if i2>0 and x[i2-1] in digits or x[i2-1] in letters:
                continue
            x=x.replace(i+",",lower(i)+"*,")
            snl.append(lower(i)+"*,")
    x=x.replace("D-","d*-")
    x=x.replace("L-","l*-")
    y=""
    for i in range(len(x)):
        buchstabe=unicode(x[i])
        if x[i] in letters:
            y+=lower(x[i])
        elif x[i] in greek1:
            y+=lower(greek2[greek1.index(x[i])])
        else:
            y+=x[i]
    x=oldcopy.copy(y)
    x=x.replace("cis","(z)")
    x=x.replace("trans","(e)")
    x=x.replace("(-)","(s)")
    x=x.replace("-s-","(s)")
    x=x.replace("?","")
    x=x.replace("!","")
    x=x.replace("delta*(","delta(").replace("lambda*(","lambda(")
    if x.startswith("s-"):
        x=x[2:]
        x="(s)"+x
    x=x.replace("ortho","o-")
    x=x.replace("meta","m-")
    x=x.replace("para","p-")
    analysereader=csv.reader(open("trivials.csv","rb"),delimiter=",")
    for row in analysereader:
        if x.startswith(row[0]):
            x=x[len(row[0]):]
            endungen=ends(x,[],["cyclo"])[1]
            if endungen=="":
                x=x+"!"
            else:
                x=x[:x.index(endungen)]+"!"+endungen
            x=lower(row[1])+endungen[0]
            ausgabe.append("?")
    if x.startswith("(") and sonderz(x)[0]=="":
            if x[0]=="(":
                x=x[1:]
                temp=analyse(x)
                endstemp=ends(temp[1][1:],[],[])
                if endstemp[0]!=[]:
                    if endstemp[0][0][0] in ("ylen","ylin","yliden","ylidin","yl","oyl","oxy","azo","azano","azeno"):
                        temp[0][0][1]=dazu(endstemp[0][0][0],endstemp[0][0][1],temp[0][0][1])
                        temp=(temp[0],")"+endstemp[1])
                lokanten,coefi,trivials=coefiwahl(coefi,1,trivials)
                for i in lokanten:
                    ausgabe.append([temp[0][0],i])
                x=temp[1][1:]
    while x!="" and x[0]!=")":
            temp=coefs(x)
            if temp[3]:
                trivials.append("greek")
            if coefi!=[]:
                if temp[3] and len(temp[0])==1:
                    trivials.append(temp[0][0])
                    trivials.remove("greek")
                    continue
                weg=ncalkan(len(coefi[-1]))
            else:
                weg=""
            if temp[0]:
                coefi.append(temp[0])
                weg=temp[2]
                x=temp[1]
                if ausgabe[-1]=="a":
                    del ausgabe[-1]
            #trivialnamen
            austausch=False
            reader=csv.reader(open("trivials.csv","rb"),delimiter=",")
            for row in reader:
                if x.startswith(row[0]):
                    austausch=True
                    x=x[len(row[0]):]
                    endungen=ends(x,[],["cyclo"]+trivials)[1]
                    if endungen=="":
                        x=x+"!"
                    else:
                        x=x[:x.index(endungen)]+"!"+endungen
                    x=lower(row[1])+x
                    ausgabe.append("?")
            if austausch:
                continue
            #Kohlenstoff-, Silicium-, etc. -ketten
            temp=sfgw(x)
            #und Hantzsch_Widmannsysteme
            temp_hwp=hantzsch_widmann(x)
            temp_hwp2=hantzsch_widmann(weg+x)
            if len(temp_hwp2[1])>len(temp_hwp[1]):
                temp_hwp=temp_hwp2
            if temp[0] != "" or temp_hwp[0]!=[]:
                if not temp_hwp[0]:
                    verlauf.append(temp[0])
                    gw=temp[0]
                    x = temp[1]
                    if gw in ("#tria","#tetra") and orstartswith(x,["asil","asil","agerman","astann","aplumb","astib"]):
                        x=x[1:]
                    if not gw.startswith("#") or orstartswith(x,["sil","asil","azan","azen","german","stann","plumb","stib"]):
                        if x.startswith("asil"):
                            x=x[1:]
                        endscoefi=[]
                        ncgw=ncalkan(gw)
                        for i in coefi:
                            for i2 in i:
                                if i2>ncgw:
                                    break
                            else:
                                endcoefi.append(i)
                        temp=ends(x,endscoefi,trivials)
                        temp,ausgabe=esterkompetenz(temp,ausgabe)
                        trivials=temp[2]
                        verlauf.append(temp[0])
                        x = temp[1]
                        endsilben=temp[0]
                    else:
                        gw=gw[1:]
                        endsilben=[]
                    if endsilben==[]:
                        if gw in ("metha","etha","propa","buta","undeca","enneadeca","icosa","henicosa"):
                            x=gw[1:-1]+x
                            continue
                        coefi.append(range(1,ncalkan(gw)+1))
                        if not "per" in trivials:
                            trivials.append("coeftest")
                else:
                    verlauf.append(temp_hwp[1])
                    gw=ncalkan(temp_hwp[0])
                    x=temp_hwp[2]
                    trivials.append("cyclo")
                    temp=ends(x,coefi,trivials)
                    temp,ausgabe=esterkompetenz(temp,ausgabe)
                    if temp[0] and "a"==ausgabe[-1]:
                        del ausgabe[-1]
                    trivials=temp[2]
                    verlauf.append(temp[0])
                    x = temp[1]
                    endsilben=temp[0]
                    i=1
                    while len(coefi[-1])<len(temp_hwp[1]):
                        if i not in coefi[-1]:
                            coefi[-1].append(i)
                            i+=1
                    zweibindig=[]
                    for i in range(len(coefi[-1])):
                        trivialsdazu=[]
                        if i in trivials2:
                            for i1 in trivials2[i]:
                                if i1.startswith("lambda"):
                                    trivialsdazu.append(i1)
                                    break
                        for i1 in trivials:
                            if i1.startswith("lambda"):
                                trivialsdazu.append(i1)
                                break
                        #noch laengst nich fertig mit System
                        ausgabe.append(System(temp_hwp[1][i],coefi[-1][i],trivialsdazu))
                        if csubs[temp_hwp[1][i]][1] in (1,2):
                            zweibindig.append(coefi[-1][i])
                    if temp_hwp[3]=="mnk":
                        i=1
                        if zweibindig!=[]:
                            if temp_hwp[0]%2==1 and min(zweibindig)%2==1:
                                i=2
                        while i<temp_hwp[0]:
                            if i in zweibindig:
                                i+=1
                            elif i+1 in zweibindig:
                                i+=2
                            else:
                                endsilben.append(["en",i])
                                i+=2
                    else:
                        endsilben.append(["an",1])
                    coefi=coefi[:-1]
                if endsilben!=[]:
                    end={}
                    for i in endsilben:
                        end=dazu(i[0],i[1],end)
                    x = temp[1]
                    if coefi==[]:
                        coefi=[[1]]
                        if not "per" in trivials and not "o(" in str(end):
                            trivials.append("coeftest")
                    for i in coefi[-1]:
                        trivials3=[]
                        trivials4=[]
                        if i in trivials2.keys():
                            for i1 in trivials2[i]:
                                if i1 in trivials:
                                    continue
                                trivials3.append(i1)
                                trivials4.append(i)
                                trivials2[i]=trivials2[i][1:]
                        if trivials4:
                            trivials4=[trivials4]
                        ausgabe.append([[ncalkan(gw),end,trivials+trivials3+trivials4],i])
                    coefi=coefi[:-1]
                    endsilben=[]
                    trivials=[]
                continue
            else:
                temp=suffixe(x)
                if temp[0] != "":
                    trytemp=praes(x)
                    if len(trytemp[0])+1>len(temp[0]):
                        verlauf.append(trytemp[0])
                        praefixe=trytemp[0]
                        x = trytemp[1]
                        if coefi==[]:
                            coefi=[[1]]
                            if not "per" in trivials:
                                trivials.append("coeftest")
                        for i in coefi[-1]:
                            trivials3=[]
                            if i in trivials2.keys():
                                for i1 in trivials2[i]:
                                    if i1 in trivials:
                                        continue
                                    trivials3.append(i1)
                                    trivials2[i]=trivials2[i][1:]
                            ausgabe.append([praefixe,i,trivials+trivials3])
                        trivials=[]
                        praefixe=[]
                        coefi=coefi[:-1]
                        continue
                    else:
                        if coefi==[]:
                            coefi=[[1]]
                            if not "per" in trivials:
                                trivials.append("coeftest")
                        for i in coefi[-1]:
                            trivials3=[]
                            if i in trivials2.keys():
                                for i1 in trivials2[i]:
                                    if i1 in trivials:
                                        continue
                                    trivials3.append(i1)
                                    trivials2[i]=trivials2[i][1:]
                            ausgabe.append([temp[0],i,trivials+trivials3,"suffix"])
                        trivials=[]
                        praefixe=[]
                        coefi=coefi[:-1]
                        x=temp[1]
                else:
                    temp=praes(x)
                    if temp[0] != "":
                        verlauf.append(temp[0])
                        praefixe=temp[0]
                        x = temp[1]
                        if coefi==[]:
                            coefi=[[1]]
                            if not "per" in trivials:
                                trivials.append("coeftest")
                        for i in coefi[-1]:
                            trivials3=[]
                            if i in trivials2.keys():
                                for i1 in trivials2[i]:
                                    if i1 in trivials:
                                        continue
                                    trivials3.append(i1)
                                    trivials2[i]=trivials2[i][1:]
                            ausgabe.append([praefixe,i,trivials+trivials3])
                        trivials=[]
                        praefixe=[]
                        coefi=coefi[:-1]
                        continue
                    else:
                        if len(x)>2 and x[:3]=="h*-":
                            for i in coefi[-1]:
                                trivials.append("H"+str(i))
                            coefi=coefi[:-1]
                            x=x[2:]
                        temp=sonderz(x)
                        if temp[0]:
                            if len(temp)==3 and temp[2]=="zucker":
                                zuckerpraefix=temp[0]
                                x=temp[1]
                                temp=ends(x,coefi,trivials,zucker=True)
                                temp,ausgabe=esterkompetenz(temp,ausgabe)
                                zuckerpraefix2=[]
                                trivials2={}
                                while temp[0]==[]:
                                    if x.startswith("o-"):
                                        x=x[2:]
                                    temp2=sonderz(x)
                                    if len(temp2)==3 and temp2[2]=="zucker":
                                        zuckerpraefix2.append(temp2[0])
                                        x=temp2[1]
                                        temp,ausgabe=esterkompetenz(temp,ausgabe)
                                    elif temp2[0] in ["l*-","d*-"]:
                                        trivials2[len(zuckerpraefix2)]=temp2[0]
                                        x=temp2[1]
                                    else:
                                        break
                                if temp[0]==[]:
                                    continue
                                zuckerends=temp[0]
                                zuckerinformation=zuckerpraefixe[zuckerpraefix]
                                gw=zuckerinformation[1]
                                gw2=0
                                vausgabe=[]
                                zuckerausgabe=[]
                                ul2=[]
                                ylstelle=0
                                for i in zuckerends:
                                    ze=i[0]
                                    if "yl"==ze:
                                        if len(coefi[-1])==1:
                                            if "greek" in trivials:
                                                ylstelle=1
                                            else:
                                                ylstelle=coefi[-1][0]
                                            coefi=coefi[:-1]
                                        else:
                                            ylstelle=1
                                    if "os"==ze:
                                        for i in zuckerends:
                                            if i[0] in ("itol","odiald","onsaeure","uronsaeure"):
                                                break
                                        else:
                                            zuckerausgabe.append(["hydroxy",gw,[]])
                                        if ul2==[]:
                                            vausgabe.append(["oxo",1,[]])
                                        else:
                                            vausgabe.append(["hydroxy",1,[]])
                                    if "ofuran"==ze:
                                        gw2=5
                                        zuckerausgabe.append(["oxa",5,[]])
                                        trivials.append("cyclo")
                                    if "opyran"==ze:
                                        gw2=6
                                        zuckerausgabe.append(["oxa",6,[]])
                                        trivials.append("cyclo")
                                    if "o-tri"==ze:
                                        gw=3
                                    if "o-tetr"==ze:
                                        gw=4
                                    if "o-pent"==ze:
                                        gw=5
                                    if "o-hex"==ze:
                                        gw=6
                                    if "o-hept"==ze:
                                        gw=7
                                    if "o-oct"==ze:
                                        gw=8
                                    if "o-non"==ze:
                                        gw=9
                                    if "ul"==ze:
                                        if i[1]==1:
                                            i[1]=2
                                        zuckerausgabe.append(["oxo",i[1],[]])
                                        ul2.append(i[1])
                                    if "itol"==ze:
                                        zuckerausgabe.append(["hydroxy",1,[]])
                                        zuckerausgabe.append(["hydroxy",gw,[]])
                                    if "odiald"==ze:
                                        vausgabe.append(["oxo",1,[]])
                                        zuckerausgabe.append(["oxo",gw,[]])
                                    if "onsaeure"==ze:
                                        zuckerausgabe.append(["hydroxy",1,[]])
                                        zuckerausgabe.append(["oxo",1,[]])
                                        zuckerausgabe.append(["hydroxy",gw,[]])
                                    if "uronsaeure"==ze:
                                        zuckerausgabe.append(["oxo",1,[]])
                                        zuckerausgabe.append(["hydroxy",1,[]])
                                        zuckerausgabe.append(["carboxy",gw,[]])
                                if "l*-" in  trivials:
                                    h=-1
                                else :
                                    h=1
                                ul=0
                                for i in zuckerinformation[0]:
                                    if ul+i in ul2:
                                        ul+=1
                                    zuckerausgabe.append(["hydroxy",ul+i,[zuckerinformation[0][i]*h]])
                                ul+=max(zuckerinformation[0].keys())
                                for i2 in range(len(zuckerpraefix2)):
                                    if i2 in trivials2:
                                        if (trivials2[i2]=="d*-" and h==-1) or  (trivials2[i2]=="l*-" and h==1):
                                            h*=-1
                                    zuckerpraefix=zuckerpraefixe[zuckerpraefix2[i2]]
                                    for i in zuckerpraefix[0]:
                                        if ul+i in ul2:
                                            ul+=1
                                        zuckerausgabe.append(["hydroxy",ul+i,[zuckerpraefix[0][i]*h]])
                                    ul+=max(zuckerinformation[0].keys())
                                cyclogw=1
                                cyclogwch=True
                                if not "cyclo" in trivials:
                                    zuckerausgabe+=vausgabe
                                else:
                                    for i in vausgabe:
                                        if i[0]=="oxo":
                                            i[0]="hydroxy"
                                            if 2 in trivials:
                                                trivials.remove(2)
                                                alphaoderbeta=2
                                            elif 3 in trivials:
                                                trivials.remove(3)
                                                alphaoderbeta=2
                                            if coefi==[] or len(coefi[-1])!=1 or coefi[-1][0] not in [2,3]:
                                                alphaoderbeta=2
                                            else:
                                                alphaoderbeta=coefi[-1][0]
                                            if alphaoderbeta==2:
                                                if "l*-" in  trivials:
                                                    i[2].append(1)
                                                else:
                                                    i[2].append(-1)
                                            else:
                                                if "l*-" in  trivials:
                                                    i[2].append(-1)
                                                    trivials.remove("l*-")
                                                else:
                                                    i[2].append(1)
                                                if "d*-" in  trivials:
                                                    trivials.remove("d*-")
                                            if cyclogwch:
                                                cyclogwch=False
                                                cyclogw=i[1]
                                        zuckerausgabe.append(i)
                                za3=False
                                zuckerausgabe2=[]
                                zuckerausgabe3=[]
                                if gw2!=0:
                                    zuckerausgabe.remove(["hydroxy",cyclogw+gw2-1,[]])
                                    if gw-gw2+2-cyclogw>0:
                                        zuckerausgabe3=[[gw-gw2+2-cyclogw,{1:["yl"]},[]],gw2-1]
                                        za3=True
                                else:
                                    gw2=oldcopy.copy(gw)
                                if "cyclo" in trivials:
                                    for i in zuckerausgabe:
                                        if i[1]>gw2-2 and i[0]!="oxa":
                                            i[1]=i[1]-gw2+2
                                            zuckerausgabe3[0].append(i)
                                        else:
                                            zuckerausgabe2.append(i)
                                else:
                                    zuckerausgabe2=oldcopy.copy(zuckerausgabe)
                                sonderausgabe=[]
                                if za3:
                                    sonderausgabe.append(zuckerausgabe3)
                                sonderausgabe+=zuckerausgabe2
                                if "l*-" in  trivials:
                                    trivials.remove("l*-")
                                elif "d*-" in  trivials:
                                    trivials.remove("d*-")
                                endungen={}
                                if ylstelle!=0:
                                    endungen[ylstelle]=["oxy","zucker"]
                                    for i in range(len(sonderausgabe)):
                                        if sonderausgabe[i][1]==ylstelle:
                                            if sonderausgabe[i][0]=="hydroxy":
                                                if 1 in sonderausgabe[i][2]:
                                                    trivials.append(1)
                                                elif -1 in sonderausgabe[i][2]:
                                                    trivials.append(-1)
                                                del sonderausgabe[i]
                                                break
                                            elif len(sonderausgabe[i])==2 and len(sonderausgabe[i][0][1])>3 and sonderausgabe[i][0][3][1]=="hydroxy":
                                                endungen[ylstelle]=["methoxy","zucker"]
                                                if 1 in sonderausgabe[i][2]:
                                                    trivials.append(1)
                                                elif -1 in sonderausgabe[i][2]:
                                                    trivials.append(-1)
                                                del sonderausgabe[i]
                                                break
                                else:
                                    endungen[1]=["an","zucker"]
                                    ausgabe+=sonderausgabe
                                    sonderausgabe=[]
                                ausgabe.append([[gw2,endungen,trivials]+sonderausgabe,1])
                                trivials=[]
                                x=temp[1]
                                continue
                            else:
                                #schon sonderz, aber kein zucker
                                verlauf.append(temp[0])
                                if type(temp[0])==str:
                                    #z.B. "cis"
                                    trivials.append(temp[0])
                                    if temp[0] in ("per","o(") and "coeftest" in trivials:
                                        trivials.remove("coeftest")
                                else:
                                    #z.B. "(1R,2S,3R,4S)"
                                    for i in temp[0].keys():
                                        if i=="*":
                                            if coefi:
                                                for i1 in coefi[-1]:
                                                    trivials2=dazu(temp[0]["*"],i1,trivials2)
                                            else:
                                                trivials.append(temp[0]["*"])
                                            continue
                                        for i1 in temp[0][i]:
                                            if i1 in ("(e)","(z)"):
                                                trivialsend.append(i1)
                                                continue
                                            trivials2=dazu(i1,i,trivials2)
                                x = temp[1]
                                continue
                        else:
                            if x[0]=="(":
                                x=x[1:]
                                temp=analyse(x)
                                if temp[1]==")":
                                    if "poly" in trivials:
                                        temp[0][0][2].append("poly")
                                    if coefi:
                                        for i in coefi[-1]:
                                            ausgabe.append([temp[0][0],i])
                                    else:
                                        ausgabe.append(temp[0])
                                    x=""
                                    break
                                endstemp=ends(temp[1][1:],[],[])
                                if endstemp[0]!=[]:
                                    if endstemp[0][0][0] in ("ylen","yliden","ylidin","ylin","yl","oyl","oxy","azo","azano","azeno"):
                                        temp[0][0][1]=dazu(endstemp[0][0][0],endstemp[0][0][1],temp[0][0][1])
                                        temp=(temp[0],")"+endstemp[1])
                                if "coeftest" in temp[0][0][2]:
                                    temp[0][0][2].remove("coeftest")
                                for i in coefi[-1]:
                                    ausgabe.append([temp[0][0],i])
                                coefi=coefi[:-1]
                                x=temp[1]
                            #Trivialnamenzusammenhalt
                            if x[0]=="!":
                                x=x[1:]
                                while type(([0]+ausgabe)[-1])==str:
                                    ausgabe.pop()
                                if "?" not in ausgabe:
                                    continue
                                elif len(ausgabe)<3:
                                    ausgabe.remove("?")
                                    continue
                                elif "?"==ausgabe[-1]:
                                    ausgabe.pop()
                                elif "?"==ausgabe[-2]:
                                    ausgabe.pop(-2)
                                else:
                                    substituentenantrivial=[]
                                    while ausgabe[-2]!="?":
                                        substituentenantrivial.append(ausgabe.pop(-2))
                                    if len(ausgabe[-1])==2:
                                        ausgabe[-1][0]+=substituentenantrivial
                                        ausgabe[-1][0][2].append("trivial")
                                    else:
                                        ausgabe[-1]+=substituentenantrivial
                                        ausgabe[-1][2].append("trivial")
                                continue
                            #loeschen des ersten Buchstabens
                            ausgabe.append(str(x[0]))
                            x = x[1:]
    if x:
        while type(ausgabe[-1])==str:
            ausgabe=ausgabe[:-1]
        ausgabe[0]=ausgabe[-1][0][0]
        ausgabe[1]=ausgabe[-1][0][1]
        ausgabe[2]=ausgabe[-1][0][2]
        ausgabe2=ausgabe[-1][0][3:]
        del ausgabe[-1]
        for i in trivials2.keys():
            for i2 in trivials2[i]:
                ausgabe[2].append(str([i2,i]))
        ausgabe[2]+=trivialsend
        ausgabe=[ausgabe+ausgabe2,1]
        return ausgabe,x
    ausgabe[2]+=trivialsend
    for i in trivials2.keys():
        for i2 in trivials2[i]:
            ausgabe[2].append(str([i2,i]))
    boese,ausgabe=boesewoerter(ausgabe)
    if boese:
        fehlerapp.Boeseswort(boese)
    ausgabe2=ausgabe[3:]
    ausgabe2.reverse()
    ausgabe=ausgabeordner(ausgabe[:3]+ausgabe2)
    return ausgabe
def ends(x,coefi,trivials,zucker=False):
    if coefi and type(coefi[-1])==list:
        coefi=coefi[-1]
    end1=("an","en","in","oxy","azo","silaz","silox","plumb","german","stann","stib","sil","enozonid","azano","azan","azeno","azen")
    end2=("olid","sultam","lacton","sulton","lactam","lacton","nitril","o(","ylidin","ylin","ylen","yliden","yl","ol","thiol","on","aldehyd","al","thial","saeureanhydrid","carbonsaeure","saeure","oat","at","azo","oxy","amid","oyl","carbonyl","ester")
    if zucker:
        end1=["yl","os","ofuran","opyran","ofuran","o-tri","o-tetr","o-pent","o-hex","o-hept","o-oct","o-non","ul","itol","odiald","onsaeure","uronsaeure"]
        end2=[]
    an=[]
    t=0
    aloesch=False
    while t==0:
        t=1
        coefi2=0
        if x=="":
            break
        if x[0]=="-":
            x=x[1:]
        if not x.startswith("diald"):
            temp2=sfgw(x)
        else:
            temp2=[]
        if temp2[0][:-1] in ["meth","eth","prop","but","undeca","enneadeca","icos","henicos"]:
            if an==[] and aloesch:
                x="a"+x
            return an,x,trivials
        if temp2[0]!="":
            if ncalkan(len(coefi))==temp2[0]:
                coefi2=range(1,ncalkan(temp2[0])+1)
            else:
                coefi2=ncalkan(temp2[0])
            x=temp2[1]
        temp=coefs(x)
        for i in end1:
            if temp[1].startswith(i):
                x=temp[1][len(i):]
                if temp[0]=="":
                    temp[0]=[1]
                    if len(coefi)==1:
                        temp[0]=coefi
                    elif coefi2!=0:
                        if coefi2==len(coefi):
                            temp[0]=coefi
                        elif type(coefi2)==type([1,2,3]):
                            temp[0]=coefi2
                else:
                    x=aloescher(x)
                for i2 in temp[0]:
                    an.append((i,i2))
                t=0
                break
        if x!="" and x[0]=="a" and not x.startswith("al")and not x.startswith("an")and not x.startswith("at")and not x.startswith("amid") and not x.startswith("azo"):
            x=x[1:]
            t=0
            aloesch=True
    t=0
    while t==0:
        t=1
        if x=="":
            break
        if x[0]=="-":
            x=x[1:]
        temp=coefs(x)
        for i in end2:
            if temp[1].startswith(i):
                if i=="ylen":
                    if len(temp[0]) in (0,2):
                        i="yl"
                        if len(temp[0])==0:
                            temp[0]=[1,2]
                if i=="ylin":
                    if len(temp[0]) in (0,3):
                        i="yl"
                        if len(temp[0])==0:
                            temp[0]=[1,2,3]
                if i=="o(":
                    if not "cyclo" in trivials:
                        continue
                    endcoef=[]
                    a=temp[1][2:temp[1].index(")")+1]
                    while a[0]!=")":
                        if a[0] in letters:
                            endcoef.append(letters.index(a[0]))
                            a=a[1:]
                        elif a[0] in digits:
                            a1=coefs(a)
                            a=a1[1]
                            endcoef.append(a1[0])
                        elif a[0] in ("-",":"):
                            a=a[1:]
                        else:
                            break
                        endcoef.append(":")
                    temp[0]=endcoef
                    temp[1]=temp[1][temp[1].index(")")+1:]
                else:
                    x=temp[1][len(i):]
                if temp[0]=="":
                    if coefi:
                        temp[0]=coefi
                        coefi=[]
                    else:
                        temp[0]=[1]
                else:
                    x=aloescher(x)
                if i=="saeure":
                    if "per" in trivials:
                        i="persaeure"
                        del trivials[trivials.index("per")]
                for i2 in temp[0]:
                    an.append((i,i2))
                t=0
                break
    if an==[] and aloesch:
        x="a"+x
    #esterkompetenz
    for i1 in range(len(an)):
        if an[i1][0]=="saeure":
            temp=sfgw(x)
            if temp[0]:
                temp2=ends(temp[1],coefi,trivials,zucker)
                for i in temp2[0]:
                    if i[0]=="ester":
                        temp2[0].remove(i)
                        an.append((temp,temp2,"#"))
                        an[i1]=("oat",an[i1][1])
                        break
    #ende der esterkompetenz
    return [an,x,trivials]

def ncalkan(x):
    num = ("","den","do","tri","tetr","pent","hex","hept","oct","non","dec","cos","triacont","tetracont","pentacont","hexacont","heptacont","octacont","nonacont","hect","dict","trict","tetract","pentact","hexact","heptact","octact","nonact","kili","dili","trili","tetrali","pentali","hexali","heptali","octali","nonali")
    nknc = [0,0,0,0]
    if type(x)== type("a"):
        if x in ("mono","monoa","metha"):
            return 1
        elif x in ("di","dia","etha"):
            return 2
        elif x in ("propa","tri"):
            return 3
        elif x=="buta":
            return 4
        elif x=="undeca":
            return 11
        elif x=="enneadeca":
            return 19
        elif x=="icosa":
            return 20
        elif x=="henicosa":
            return 21
        elif x=="di":
            return 2
        elif x in ["bis","tris","tetrakis","pentakis","hexakis","heptakis","oktakis","nonakis"]:
            return ["bis","tris","tetrakis","pentakis","hexakis","heptakis","oktakis","nonakis"].index(x)+2
        if x.endswith("lia"):
            for i in range(1,10):
                if x.endswith(num[27+i]+"a"):
                    nknc[3]=i
                    break
            x=x[:-len(num[27+nknc[3]])-1]
        if x.endswith("cta") and not x.endswith("octa"):
            for i in range(1,10):
                if x.endswith(num[18+i]+"a"):
                    nknc[2]=i
                    break
            x=x[:-len(num[18+nknc[2]])-1]
        if x.endswith("conta") or x.endswith("ca") or x.endswith("sa"):
            for i in range(1,10):
                if x.endswith(num[9+i]+"a"):
                    nknc[1]=i
                    break
            x=x[0:-len(num[9+nknc[1]])-1]
        for i in range(1,10):
            if x.endswith(num[i]+"a"):
                nknc[0]=i
                break
            if x[-2:]=="do":
                nknc[0]=2
            if x[-3:] in ("den","un","mono"):
                nknc[0]=1
        return 1000*nknc[3]+100*nknc[2]+10*nknc[1]+nknc[0]
    elif type(x)== type(3):
        if x==1:
            return "mono"
        elif x==2:
            return "di"
        elif x==3:
            return "tri"
        elif x==11:
            return "undecan"
        elif x==19:
            return "enneadeca"
        elif x==20:
            return "icosa"
        elif x==21:
            return "henicosa"
        b = str(x)
        for i in range(len(b)-1,-1,-1):
            nknc[i]=int(x/10**i)
            x-=nknc[i]*10**i
        x=""
        if nknc[0]!=0:
                x=x+num[nknc[0]]
                if nknc[i]!=2 and nknc[i]!=3:
                    x+="a"
        for i in range(1,4):
            if nknc[i]!=0:
                x +=num[nknc[i]+i*9]+"a"
        return x
def sfgw(x):
    num = ["","den","do","tri","tetr","pent","hex","hept","oct","non","dec","cos","triacont","tetracont","pentacont","hexacont","heptacont","octacont","nonacont","hect","dict","trict","tetract","pentact","hexact","heptact","octact","nonact","kili","dili","trili","tetrali","pentali","hexali","heptali","octali","nonali"]
    astr = ""
    an = ["mono","di","tri","tetra","meth","eth","prop","but","undec","enneadec","icos","henicos"]
    an2 = ["dec","hect","kili","cos","dict","dili"]
    gvs = ["acont","act","ali"]
    if orstartswith(x,["silan","azan","germanan","stannan","plumban","stiban"]):
        x="mono"+x
    x=" " + x + "ENDE"
    while x != "ENDE":
        if x=="anonENDE":
            return [astr,"anon"]
        f = x[:1]
        x = x[1:]
        a1 = 12
        for i in range(1,37):
            if x.startswith(num[i]):
                a1 = i
                break
        if a1 == 12:
            a2=6
            for i in range(len(an2)):
                if x.startswith(an2[i]):
                    a2=i
                    astr=astr+an2[a2]+"a"
                    x=x[len(an2[a2]):]
                    break
            if a2!=6:
                    continue
            if astr == "":
                for i in range(len(an)):
                    if x.startswith(an[i]):
                        return [an[i] + "a",x[len(an[i]):-4]]
                return ["",x[:-4]]
            else:
                if astr in ("mono","do","tria","tetra"):
                     astr="#"+astr
                return [astr,f+x[:-4]]
        x = x[len(num[a1]):]
        if a1==3 and not x.startswith("aconta") or a1==2:
            x="a"+x
        a2=3
        for i in range(0,3):
            if x.startswith(gvs[i]):
                a2=i
                break
        if a2!=3:
            x = x[len(gvs[a2]):]
        astr = astr + num[((a2+1)%4)*9+a1]
        if num[((a2+1)%4)*9+a1] not in ("den","do"):
            astr+="a"
        elif num[((a2+1)%4)*9+a1]=="den":
            x="a"+x
    if astr in ("mono","dia","tria","tetra"):
        astr="#"+astr
        return ["",x[:-4]]
    return [astr,x[:-4]]