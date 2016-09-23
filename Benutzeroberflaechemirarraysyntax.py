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
global valenzep2,info,sizeC,sizeB,sizeCprop,opacitychosen,cyc,lengthB,AllIn2,valenzep2,csubs,greek1,greek2,snl,Polyscale,mi,zuckerpraefixe
from atome import atomlist
class atomklasse:
    def __init__(self,ordnungszahl,color,weight,radius,valenz,en):
        self.ordnungszahl = ordnungszahl
        self.color = color
        self.weight = weight
        self.radius = radius
        self.en = en
        self.valenz = valenz
class atom_on_screen:
    def __init__(self,sym,oxz,hyb,obj):
        self.sym = sym
        self.oxz = oxz
        self.hyb = hyb
        self.obj = obj
H = atomklasse(1,(1,1,1),1,1.24,1,2.2)
xx = atomklasse(0,(1,1,1),-1,0,1,0)
for i in atomlist:
    exec("symbol"+i+"=atomklasse("+str(atomlist[i][0])+","+str(atomlist[i][1])+","+str(atomlist[i][2])+","+str(atomlist[i][3])+","+str(atomlist[i][7])+","+str(atomlist[i][6])+")")
bt=1
mi=3
def info(source,key):
    key=ohnezahlen(key)
    if source == "atom":
        s=atomlist[key]
    elif source == "symbol":
        s=name[key]
    elif source == "praefix":
        s=praefix[key]
    elif source == "suffix":
        s=suffix[key]
    return s
def en(x):
    x=ohnezahlen(x)
    return eval("symbol"+str(x)+".en")
def valenz(x):
    x=ohnezahlen(x)
    return eval("symbol"+str(x)+".valenz")
def oxidationszahlengenerator(x):
    x=oxidationszahl(x)
    x=[x[0]]+oxzahlordner(x)
    return x
def oxzahlordner(x):
    geordneteliste=[]
    for i in x[1:]:
        geordneteliste.append(i[0])
    for i in x[1:]:
        geordneteliste+=oxzahlordner(i)
    return geordneteliste
def oxidationszahl(x,y=None):
    currenten=en(x[0])
    currentvalenz=valenz(x[0])
    elektronen=0
    zaehler=0
    dazulist=[]
    altsyntax=[]
    if y:
        a=2
        b=[y]
    else:
        a=1
        b=[]
    for i in x[a:]+b:
        if "@" in i[0]:
            i2=i[0][1:]
            while i2[0] in string.digits:
                i2=i2[1:]
            en2=en(i2[0])
        else:
            en2=en(i[0])
        if en2<currenten:
            elektronen+=i[1][1]*2
        elif en2==currenten:
            elektronen+=i[1][1]
        zaehler+=i[1][1]*2
        if len(i[1])>2:
            if "@" in i[0]:
                altsyntax.append([-10])
            else:
                altsyntax.append(oxidationszahl(i,[x[0],[0,i[1][1]]]))
    if zaehler!=currentvalenz and x[0]!="H" and zaehler<8:
        for i in range(0,int(currentvalenz-zaehler/2.),2):
            elektronen+=2
    return [currentvalenz-elektronen]+altsyntax
def Visual(x,position=vector(0,0,0),axxxis=vector(0,1,0),winkel=0,pos=[],oldaxis=vector(0,0,-1),erstes=False):
    nzz=[]
    global lokanten,cislist,translist,AllIn,YL,Yl1,Yl2,AllAtoms,MFB,sizeC,sizeB,sizeCprop,lengthB,AllIn2,Vyl,valenzep2,nachdrehen
    if erstes:
        saettigungsbeilage=[x[1][0]]
        if len(x[1])>3:
            if x[1][2][0][0]=="@" and len(x[1][3])>3:
                x[1][3][2][1][2]+=2*pi/3
        if x[1][0] !="H" and not "@" in x[1][0]:
            alpha=[0]
            nzz.append(1)
        YL={}
        valenzep2=[]
        AllIn=[]
        AllIn2=[]
        AllAtoms=[]
        Yl1=[]
        Yl2=[]
        Vyl=[]
        cislist=[]
        translist=[]
        nachdrehen=[]
        MFB=[]
        atominfo=atom_color(x[0])
        AllIn2.append(x[0])
        AllIn.append([position,atominfo[3]])
        lokanten=[mitzahlen(x[0])]
        x2=x[0]
        AllAtoms.append(sphere(pos=position,color=atominfo[0],radius=atominfo[1]*sizeC+sizeCprop,opacity=opacitychosen))
    else:
        saettigungsbeilage=[0]
    for i in range(2,len(x)):
        saettigungsbeilage.append(x[i][0])
        if x[i][0] != "H" and "@" not in x[i][0]:
            nzz.append(i)
    konfig=[]
    alpha=[]
    cistrans=[]
    winkel=0
    konfigdic2=[0]
    if type(x[1][1])==type(1):
        konfig.append(x[1][1])
    else:
        konfig.append(x[1][1][1])
        alpha.append(x[1][1][0])
        if x[1][1][0]!=0:
                konfigdic2[0]=1
        if x[1][1][2]!=0:
            if type(x[1][1][2])==type("cis"):
                if x[1][1][2][0]=="a":
                    alpha.append(eval(x[1][1][2][1:]))
                elif x[1][1][2][:3]=="cis":
                    if int(x[1][1][2][3:])<=len(cislist):
                        cistrans=[cislist[int(x[1][1][2][3:])-1],1,1]
                    else:
                        cistrans=[int(x[1][1][2][3:]),1,i,1]
                else:
                    if int(x[1][1][2][5:])<=len(translist):
                        cistrans=[translist[int(x[1][1][2][5:])-1],2,1]
                    else:
                        cistrans=[int(x[1][1][2][5:]),2,i,1]
            else:
                if abs(x[1][1][2])!=pi and x[1][1][2]!=0:
                    konfigdic2[0]=1
                if x[1][1][1]==1 or abs(x[1][1][2])==pi:
                    winkel=winkel+x[1][1][2]
    for i in range(2,len(x)):
        if type(x[i][1])!=type(1):
            konfigdic2.append(0)
            konfig.append(x[i][1][1])
            alpha.append(x[i][1][0])
            if x[i][1][0]!=0:
                konfigdic2[i-1]=1
            if x[i][1][2]!=0:
                if type(x[i][1][2])==type("cis"):
                    if x[i][1][2][0]=="a":
                        alpha.append(eval(x[i][1][2][1:]))
                    elif x[i][1][2][:3]=="cis":
                        if int(x[i][1][2][3:])<=len(cislist):
                            cistrans=[cislist[int(x[i][1][2][3:])-1],1,i]
                        else:
                            cistrans=[int(x[i][1][2][3:]),1,i,1]
                    else:
                        if int(x[i][1][2][5:])<=len(translist):
                            cistrans=[translist[int(x[i][1][2][5:])-1],2,i]
                        else:
                            cistrans=[int(x[i][1][2][5:]),2,i,1]
                else:
                    if abs(x[i][1][2])!=pi and x[i][1][2]!=0:
                        konfigdic2[i-1]=1
                    if x[i][1][2]!=0 and x[i][1][1]==1 or abs(x[i][1][2]+2*pi/3*(i-2))==pi:
                        winkel=winkel+x[i][1][2]#+2*pi/3*(i-2)
        else:
            konfig.append(x[i][1])
    if x[1][1]==2 and winkel not in (pi,-pi):
        winkel=0
    pos=atom(x[0],saettigungsbeilage,position,axxxis,konfig,winkel,alpha=alpha,ct=cistrans,oldaxis=oldaxis,konfigdic2=konfigdic2)
    pos2=pos[1]
    valenzen2=pos[2]
    testebitte=pos[3]
    pos=pos[0]
    if len(cistrans)==4:
        if cistrans[1]==1:
            cislist.append(pos[cistrans[3]-1])
        else:
            translist.append(pos[cistrans[3]-1])
    Yl=[]
    for i in range(len(x[1:])):
        if type(x[i+1][0])!=str:
            continue
        if x[i+1][1][2]==10*pi:
            nachdrehen.append(len(MFB)-len(x)+i+1)
    for i in range(len(nzz)):
        pos3=Visual(x[nzz[i]],pos[nzz[i]-1],position-pos[nzz[i]-1],winkel,pos,axxxis)
        yl=pos3[1]
        valenzen=pos3[2]
        pos3=pos3[0]
        if len(x[nzz[i]][1])==3 and x[nzz[i]][1][1]==1:
            if pos[nzz[i]-1]-position in Yl1:
                Yl2[Yl1.index([pos[nzz[i]-1]-position,position])].append(n)
                Vyl[Yl1.index([pos[nzz[i]-1]-position,position])].append(valenzen)
            else:
                Yl.append(len(Yl1))
                Yl1.append([pos[nzz[i]-1]-position,position])
                Yl2.append([])
                Vyl.append([])
                for n in pos3:
                    Yl2[-1].append(n)
                for n in valenzen:
                    Vyl[-1].append(n)
            if yl!=[]:
                n2=[]
                YL.__init__({len(Yl1):yl})
        pos2+=pos3
        valenzen2+=valenzen
        for n in yl:
            Yl.append(n)
    return pos2,Yl,valenzen2
def gebundenan(x,y):
    for i in x[1:]:
        if i[0]==y:
            return x[0]
        if len(i)>1:
            a=gebundenan(i,y)
            if a:
                return a
def syntuxzuatomzeichnen(displaychosen,x,a1,a2,a3,a4,a5,a6,parent,bindungsg,keilstrich=False,wasserstoff=False):
    global bindungsg2,YL,Yl1,Yl2,AllIn,AllIn2,AllAtoms,MFB,sizeC,sizeB,sizeCprop,lengthB,Vyl,valenzep2,bt,cislist,translist,saettigungsbeilage,opacitychosen,opacitychosen2,lokanten,wasserstoffonoff,nachdrehen,MFBausrichtung
    #Drehachsen                 : Vektor
    #Ladung                     : Ganzzahl
    #Position                   : Vektor
    #Elementsymbol              : String
    #Atom                       : Position des Objekts in AllAtoms
    #Atom auf dem Bildschirm    : Objekt (primitive)

    #Yl1: "kritische" Bindungen um die gedreht werden soll
        #Datentyp: [ [ Drehachse , Augangsposition ] , ...]

    #Yl2: Alle geladenen Elemente hinter der kritischen Bindung
        #Datentyp: [ [ [ Position , Ladung] , ... ] , ... ]

    #YL: Bindungen, die sich bei Drehung um eine vorhergehende Bindung verändern kÃ¶nnen (Bezugsklärung bei komplexeren Verkettungen)
        #Datentyp: {"kritische" Bindung : Bindungen die verändert werden }

    #Vyl: Alle geladenen Elemente ( Wasserstoff, Valenzelektronen , Bindungen) , die sich hinter der kritischen Bindung befinden
        #Datentyp: [ [ [ Position des Elements, Ladung ] , ... ] , ...geladenen Elemente der anderen Bindungen ]
    #valenzep2: ALLE geladenen Elemente
        #Datentyp: [ [ Position des Elements , Ladung] ]

    #sizeC: relative Größe eines Atoms (Kohlenstoff als Maßstab)
        #Datentyp: Float

    #sizeCprop: Summand der zum Radius eines Atoms addiert wird
        #Dartentyp: Float

    #sizeB: Bindungsradius
        #Datentyp: Float

    #lengthB: Bindungslänge
        #Datentyp: Float

    #AllIn: Informationen über ALLE Atome auf dem Bildschirm
        #Datentyp: [ [ Position , Anzahl AuÃŸenelektronen (Float) ],... ]

    #AllIn2: Alle Atome auf dem Bildschirm
        #Datentyp: [ Elementsymbol ,...]

    #MFB: Alle Bindungen
        #Datentyp: [ [ Atom 1 , Atom 2 , Art der Bindung , [ Elementsymbol 1 , Elementsymbol 2 ] ] ]

    #AllAtoms: ALLE Atome als Objekte
        #Datentyp: [ Atom auf dem Bildschirm 1 , ...]
    sizeC=a1
    sizeB=a2
    sizeCprop=a3
    lengthB=a4
    bindungsg2=bindungsg
    MFBausrichtung=[]
    wasserstoffonoff=wasserstoff
    opacitychosen=a5
    opacitychosen2=a6
    displaychosen.select()
    Visual(x,erstes=True)#zeichnet nach der Umschreibung
    #***WICHTIG*** AllIn ist die Variable, bei der Atompositionen verschoben werden
    #***WICHTIG*** AllAtoms wird erst spaeter angeopasst
    zahlen=[0]+zahlenbeschreibung(x)[0]
    for i in range(len(nachdrehen)):
        pseudoAtome=[]
        zahl="0"+str(len(nachdrehen)-i-1)
        for i2 in range(len(AllIn2)-1,1,-1):
            if zahl in AllIn2[i2]:
                pseudoAtome.append(AllIn[i2][0])
                AllIn2[i2]=="xx"
                if len(pseudoAtome)==2:
                    davor=AllIn[gebundenan(zahlen,i2)][0]
                    wunschort=pseudoAtome[1]-davor
                    if abs(wunschort-pseudoAtome[0])>0.1:
                        position=AllIn[MFB[nachdrehen[i]][0]][0]
                        achse=AllIn[MFB[nachdrehen[i]][1]-1][0]-position
                        drehpunkt=proj(davor-position,achse)
                        winkel=diff_angle(davor-drehpunkt-position,pseudoAtome[0]-drehpunkt-position)
                        drehzahl=allenachzahl(zahlen,MFB[nachdrehen[i]][1]-1)
                        drehenachzahl(drehzahl,winkel,achse,position)
                    pseudoAtome=[]
    for i in range(len(AllIn2)):
        if AllIn2[i][0]=="x":
            AllIn2[i]="xx"
    #Strukturidealisierung
    if bt!=0:
        Gesamt=0
        if Yl1!=[]:
            Gesamt=50./len(Yl1)/int((2*pi/(pi/36./bt)))
            Wert=0
        wait=wx.ProgressDialog("Chython - Bitte warten",u"Die Struktur des Moleküls wird berechnet",maximum=101,parent=parent,style=wx.PD_APP_MODAL)
        wait.Show()
        for q in range(2):
            for i1 in range(len(Yl1)-1,-1,-1):
                #i1 = kritische Bindung
                sum2=0
                w=0
                V=[]
                for i4 in valenzep2:
                    if i4 not in Vyl[i1]:
                        V.append(i4)
                Wert+=Gesamt
                wait.Update(Wert)
                for i3 in Vyl[i1]:
                    for i4 in V:
                        if drehmesser(i3[1],i4[1])==0:
                            continue
                        sum2+=lengthB*1./(mag(i3[0]-i4[0])*drehmesser(i3[1],i4[1]))
                for i2 in arange(pi/36./bt,2*pi,pi/36./bt):
                    Wert+=Gesamt
                    wait.Update(Wert)
                    sum1=0
                    for i3 in Vyl[i1]:
                        h=i3[0]-Yl1[i1][1]
                        for i4 in V:
                            if drehmesser(i3[1],i4[1])==0:
                                continue
                            sum1+=lengthB*1./(mag(rotate(h,i2,Yl1[i1][0])+Yl1[i1][1]-i4[0])*drehmesser(i3[1],i4[1]))
                    if sum1>sum2:
                        #wenn sum1 günstiger ist als alle vorhergehenden Werte wird sum1 -> sum2
                        sum2=sum1
                        #sum2 ist die günstigste Drehung
                        w=i2
                        #w = Gradzahl bei Drehung
                #Hier ist die günstigste Drehung bekannt und in w gespeichert
                if i1+1 in YL:
                #Alle kritischen Bindungen, die beeinflusst werden kÃ¶nnen, werden angepasst
                    for i3 in YL[i1+1]:
                        iplus1=rotate(Yl1[i3][1]+Yl1[i3][0]-Yl1[i1][1],w,Yl1[i1][0])+Yl1[i1][1]
                        Yl1[i3][1]=rotate(Yl1[i3][1]-Yl1[i1][1],w,Yl1[i1][0])+Yl1[i1][1]
                        Yl1[i3][0]=iplus1-Yl1[i3][1]
                for i3 in range(len(Yl2[i1])):
                    #Alle Atome, die sich hinter der Drehung befinden, werden gedreht
                    AllIn[AllIn.index(Yl2[i1][i3])][0]=rotate(Yl2[i1][i3][0]-Yl1[i1][1],w,Yl1[i1][0])+Yl1[i1][1]
                for i3 in range(len(Vyl[i1])):
                    #Alle geladenen Elemente, die sich hinter der Bindung befinden, werden gedreht
                    Vyl[i1][i3][0]=rotate(Vyl[i1][i3][0]-Yl1[i1][1],w,Yl1[i1][0])+Yl1[i1][1]
        wait.Destroy()
        #Alle Drehungen sind abgeschlossenen
        #Die Positionen der Objekte werden angepasst
    #hier wird AllAtoms angepasst
    for i in range(len(AllIn)):
        AllAtoms[i].pos=AllIn[i][0]
    #Die Bindungen werden gezeichnet
    object_bindungen=[]
    for i in MFB:
        if i[2]==2:
            object_bindungen.append(mehrfachbindung(AllIn[i[0]][0],AllIn[i[1]-1][0],i[2],i[3],i[4],keilstrich=keilstrich))
        else:
            object_bindungen.append(mehrfachbindung(AllIn[i[0]][0],AllIn[i[1]-1][0],i[2],i[3],keilstrich=keilstrich))
    for i in MFBausrichtung:
        object_bindungen[i[0]].up=rotate(AllAtoms[i[1]].pos,pi/2,object_bindungen[i[0]].axis)
    return AllIn2,AllAtoms,oxidationszahlengenerator(x),lokanten
def zahlenbeschreibung(x,n=0):
    zahlen=[]
    nzz=[]
    for i in range(len(x[1:])):
        if type(x[i+1][0])==str:
            n+=1
            zahlen.append([n])
            if len(x[i+1])>2:
                nzz.append([i+1,len(zahlen)-1])
    for i in nzz:
        a,n=zahlenbeschreibung(x[i[0]],n)
        zahlen[i[1]]+=a
    return zahlen,n
def allenachzahl(x,zahl):
    if x[0]==zahl:
        return x
    else:
        for i in x[1:]:
            a=allenachzahl(i,zahl)
            if a:
                return a
def drehenachzahl(x,winkel,achse,position):
    for i in x[1:]:
        AllIn[i[0]][0]=rotate(AllIn[i[0]][0]-position,winkel,achse)+position
        drehenachzahl(i,winkel,achse,position)
def drehmesser(a,b):
    if a==-1 and b==-1:
        return -1
    if a==-2 and b==-2:
        return -2
    if a>0 and b==-2:
        return a*2
    if a==-2 and b>0:
        return b*2
    if a>0 and b>0:
        return -(a+b)/2
    return 0
def atom_color(Symbol): #abk = Abkuerzung des Elements
    Symbol=ohnezahlen(Symbol)
    d = info("atom",Symbol)
    return [d[1],d[3],d[2],d[4]]
def mehrfachbindung(pos,axis,art,atome,pointon=0,keilstrich=False):
    global sizeC,sizeB,sizeCprop,lengthB,opacitychosen2,bindungsg2,wasserstoffonoff
    f=frame()
    atom1=atom_color(atome[0])
    atom2=atom_color(atome[1])
    atom1[0]=(atom1[0][0],atom1[0][1],atom1[0][2])
    atom2[0]=(atom2[0][0],atom2[0][1],atom2[0][2])
    laenge=lengthB-(atom1[1]*sizeC+sizeCprop)-(atom2[1]*sizeC+sizeCprop)
    verbindungsstueck=0
    if art==2:
        if pointon==0:
            pointon=sphere(pos=pos+vector(0,1,0),radius=0)
        axis=axis-pos
        n1=curve(frame=f,x=arange(-lengthB/2.,-lengthB/2.+laenge/2.+atom1[1]*sizeC+sizeCprop+verbindungsstueck,0.5)+lengthB/2.,radius=sizeB,color=atom1[0])
        n1.y=(lengthB**2-(n1.x-lengthB/2.)**2)**.5-sin(pi/3)*lengthB
        n1.z=n1.x*0
        n3=curve(frame=f,x=arange(lengthB/2.,lengthB/2.-laenge/2.-atom1[1]*sizeC-sizeCprop-verbindungsstueck,-0.5)+lengthB/2.,radius=sizeB,color=atom2[0])
        n3.y=n1.y
        n3.z=n1.x*0
        if n3.x[-1]!=n1.x[-1]:
            #nicht richtig verbundene curves
            verbindungsstueck+=0.5
            n1=curve(frame=f,x=arange(-lengthB/2.,-lengthB/2.+laenge/2.+atom1[1]*sizeC+sizeCprop+verbindungsstueck,0.5)+lengthB/2.,radius=sizeB,color=atom1[0])
            n1.y=(lengthB**2-(n1.x-lengthB/2.)**2)**.5-sin(pi/3)*lengthB
            n1.z=n1.x*0
            n3=curve(frame=f,x=arange(lengthB/2.,lengthB/2.-laenge/2.-atom1[1]*sizeC-sizeCprop-verbindungsstueck,-0.5)+lengthB/2.,radius=sizeB,color=atom2[0])
            n3.y=n1.y
            n3.z=n1.x*0
        n2=curve(frame=f,x=arange(-lengthB/2.,-lengthB/2.+laenge/2.+atom1[1]*sizeC+sizeCprop+verbindungsstueck,0.5)+lengthB/2.,radius=sizeB,color=atom1[0])
        n2.y=-n1.y
        n2.z=n1.x*0
        n4=curve(frame=f,x=arange(lengthB/2.,lengthB/2.-laenge/2.-atom1[1]*sizeC-sizeCprop-verbindungsstueck,-0.5)+lengthB/2.,radius=sizeB,color=atom2[0])
        n4.y=-n1.y
        n4.z=n2.x*0
    elif art==3:
        axis=axis-pos
        n1=curve(frame=f,x=arange(-lengthB/2.,-lengthB/2.+laenge/2.+atom1[1]*sizeC+sizeCprop+verbindungsstueck,0.5)+lengthB/2.,radius=sizeB,color=atom1[0])
        n1.y=(lengthB**2-(n1.x-lengthB/2.)**2)**.5-sin(pi/3)*lengthB
        n1.z=n1.x*0
        n4=curve(frame=f,x=arange(lengthB/2.,lengthB/2.-laenge/2.-atom1[1]*sizeC-sizeCprop-verbindungsstueck,-0.5)+lengthB/2.,radius=sizeB,color=atom2[0])
        n4.y=(lengthB**2-(n1.x-lengthB/2.)**2)**.5-sin(pi/3)*lengthB
        n4.z=n1.x*0
        if n4.x[-1]!=n1.x[-1]:
            verbindungsstueck+=0.5
            n1=curve(frame=f,x=arange(-lengthB/2.,-lengthB/2.+laenge/2.+atom1[1]*sizeC+sizeCprop+verbindungsstueck,0.5)+lengthB/2.,radius=sizeB,color=atom1[0])
            n1.y=(lengthB**2-(n1.x-lengthB/2.)**2)**.5-sin(pi/3)*lengthB
            n1.z=n1.x*0
            n4=curve(frame=f,x=arange(lengthB/2.,lengthB/2.-laenge/2.-atom1[1]*sizeC-sizeCprop-verbindungsstueck,-0.5)+lengthB/2.,radius=sizeB,color=atom2[0])
            n4.y=(lengthB**2-(n1.x-lengthB/2.)**2)**.5-sin(pi/3)*lengthB
            n4.z=n1.x*0
        n2=curve(frame=f,x=arange(-lengthB/2.,-lengthB/2.+laenge/2.+atom1[1]*sizeC+sizeCprop+verbindungsstueck,0.5)+lengthB/2.,radius=sizeB,color=atom1[0])
        n2.y=-n1.y*sin(pi/6.)
        n2.z=-n1.y*cos(pi/6.)
        n3=curve(frame=f,x=arange(-lengthB/2.,-lengthB/2.+laenge/2.+atom1[1]*sizeC+sizeCprop+verbindungsstueck,0.5)+lengthB/2.,radius=sizeB,color=atom1[0])
        n3.y=-n1.y*sin(pi/6.)
        n3.z=n1.y*cos(pi/6.)
        n5=curve(frame=f,x=arange(lengthB/2.,lengthB/2.-laenge/2.-atom1[1]*sizeC-sizeCprop-verbindungsstueck,-0.5)+lengthB/2.,radius=sizeB,color=atom2[0])
        n5.y=-n1.y*sin(pi/6.)
        n5.z=-n1.y*cos(pi/6.)
        n6=curve(frame=f,x=arange(lengthB/2.,lengthB/2.-laenge/2.-atom1[1]*sizeC-sizeCprop-verbindungsstueck,-0.5)+lengthB/2.,radius=sizeB,color=atom2[0])
        n6.y=-n1.y*sin(pi/6.)
        n6.z=n1.y*cos(pi/6.)
    elif art==1:
        if wasserstoffonoff and "H" in atome:
            laenge=lengthB*0.7-(atom1[1]*sizeC+sizeCprop)-(atom2[1]*sizeC+sizeCprop)
        enatom1=en(atome[0])
        enatom2=en(atome[1])
        if bindungsg2:
            plus1=norm(axis-pos)*abs((atom1[1]*sizeC+sizeCprop)**2-sizeB**2)**.5
            plus2=norm(pos-axis)*abs((atom2[1]*sizeC+sizeCprop)**2-sizeB**2)**.5
        else:
            plus1=(0,0,0)
            plus2=(0,0,0)
        if keilstrich and abs(enatom1-enatom2)>0.4:
            if enatom1-enatom2>0.4:
                cone(pos=pos+plus1,axis=axis-pos,radius=sizeB*1.5,color=atom1[0])
            else:
                cone(pos=axis-plus2,axis=pos-axis,radius=sizeB*1.5,color=atom2[0])
        else:
            n1=cylinder(pos=pos+plus1,axis=norm(axis-pos)*(laenge/2.+atom1[1]*sizeC+sizeCprop)-plus1,radius=sizeB,color=atom1[0],opacity=opacitychosen2)
            n2=cylinder(pos=axis+plus2,axis=norm(pos-axis)*(laenge/2.+atom2[1]*sizeC+sizeCprop)-plus2,radius=sizeB,color=atom2[0],opacity=opacitychosen2)
    if art==1:
        f=[n1,n2]
    else:
        f.axis=axis
        f.pos=pos
    return f
def atom(natom,saettigungsbeilage,posn,axxis,konfigdic,winkel=0,alpha=[],p=0,ct=0,oldaxis=vector(0,0,-1),konfigdic2=[0,0,0,0,0,0,0,0]):
        global MFBausrichtung,AllIn,AllIn2,AllAtoms,MFB,sizeC,sizeB,sizeCprop,lengthB,valenzep2,opacitychosen,lokanten,wasserstoffonoff
        natom=ohnezahlen(natom)
        axxis[0]*=-1
        axxis[2]*=-1
        atominfo=atom_color(natom)
        drehwinkel=diff_angle2((0,1,0),axxis)
        achse=cross(axxis,(0,1,0))
        atominfo2=[]
        testebitte=[]
        valenzep=[]
        laengen=[]
        for i in saettigungsbeilage:
            if i==0:
                atominfo2.append(0)
            elif "@" in i:
                lokanten.append("")
                atominfo2.append(([0,0,0],0,0,0))

            else:
                lokanten.append(mitzahlen(i))
                i=ohnezahlen(i)
                atominfo2.append(atom_color(i))
            if wasserstoffonoff and i=="H":
                laengen.append(.7)
            else:
                laengen.append(1)
        laengen+=[0,0,0,0,0,0]
        pos=range(len(konfigdic))
        pos[0]=posn+rotate((0,lengthB*laengen[0],0),drehwinkel,achse)
        valenzen=valenz(natom)
        if atominfo2[0]!=0:
            AllAtoms.append(sphere(pos=pos[0],color=atominfo2[0][0],radius=atominfo2[0][1]*sizeC+sizeCprop,opacity=opacitychosen))
        if len(konfigdic)==4 or (konfigdic==[1,1,1] and  valenzen>4) or (konfigdic==[1,1] and valenzen>5) or konfigdic==[1]:
            #Anordnung wie Methan oder Ammoniak oder Wasser oder Fluorid
            axxis[0]*=-1
            axxis[2]*=-1
            oldaxis[0]*=-1
            oldaxis[2]*=-1
            a=diff_angle2(oldaxis,-axxis)-pi/2.
            oldaxis=rotate(oldaxis,a,cross(oldaxis,-axxis))
            if absolute(diff_angle2(oldaxis,-axxis)-pi/2.)>.1:
                oldaxis=rotate(oldaxis,-2.*a,cross(oldaxis,-axxis))
            axxis[0]*=-1
            axxis[2]*=-1
            pws=diff_angle2(oldaxis,rotate(vector(0,0,-1),drehwinkel,achse))
            if absolute(diff_angle2(oldaxis,rotate(rotate(vector(0,0,-1),pws,(0,1,0)),drehwinkel,achse)))<0.2:
                winkel=winkel+pws%(2*pi)
            else:
                winkel=winkel-pws%(2*pi)
            pos=[pos[0]]+range(3)
            for i in range(2-len(alpha)):
                alpha.append(radians(109.5))
            if alpha[0]==0:
                alpha[0]=radians(109.5)
            if alpha[1]==0:
                alpha[1]=radians(109.5)
            pos[1]=vector(0,-cos(pi-alpha[0])*lengthB*laengen[1],-sin(pi-alpha[0])*lengthB*laengen[1])
            pos[2]=posn+rotate(rotate(norm(pos[1]+vector(0,lengthB,0))*cos(alpha[1]/2.)*-lengthB*laengen[2]+norm(cross(pos[1],vector(0,lengthB*laengen[2],0)))*sin(alpha[1]/2.)*lengthB*laengen[2],winkel,(0,1,0)),drehwinkel,achse)
            pos[3]=posn+rotate(rotate(norm(pos[1]+vector(0,lengthB,0))*cos(alpha[1]/2.)*-lengthB*laengen[3]-norm(cross(pos[1],vector(0,lengthB*laengen[3],0)))*sin(alpha[1]/2.)*lengthB*laengen[3],winkel,(0,1,0)),drehwinkel,achse)
            pos[1]=posn+rotate(rotate(pos[1],winkel,(0,1,0)),drehwinkel,achse)
            if len(ct)==3:
                    p=[]
                    for i in (1,2,3):
                        if konfigdic2[i]==1:
                            continue
                        p.append(i)
                    if len(p)>1:
                        p1=mag(ct[0]-pos[p[0]])
                        p2=mag(ct[0]-pos[p[1]])
                        if p1>p2:
                            if ct[1]==2:
                                pos[p[0]],pos[p[1]]=pos[p[1]],pos[p[0]]
                        else:
                            if ct[1]==1:
                                pos[p[0]],pos[p[1]]=pos[p[1]],pos[p[0]]
            if len(konfigdic)==1:
                valenzep.append([(pos[1]-posn)/4.+posn,-2])
            else:
                AllAtoms.append(sphere(pos=pos[1],color=atominfo2[1][0],radius=atominfo2[1][1]*sizeC+sizeCprop,opacity=opacitychosen))
            if len(konfigdic)in(1,2):
                valenzep.append([(pos[2]-posn)/4.+posn,-2])
            else:
                AllAtoms.append(sphere(pos=pos[2],color=atominfo2[2][0],radius=atominfo2[2][1]*sizeC+sizeCprop,opacity=opacitychosen))
            if len(konfigdic)!=4:
                valenzep.append([(pos[3]-posn)/4.+posn,-2])
                if len(konfigdic)==3:
                   testebitte.append([pos[2]-posn+pos[3],pos[2]])
            else:
                AllAtoms.append(sphere(pos=pos[3],color=atominfo2[3][0],radius=atominfo2[3][1]*sizeC+sizeCprop,opacity=opacitychosen))
        elif ((len(konfigdic)==3 and sum(konfigdic) not in (0,1,2,3)) or (len(konfigdic)==2 and sum(konfigdic)==3) or konfigdic==[2]) or (konfigdic==[1,1,1] and  valenzen<=4):
                axxis[0]*=-1
                axxis[2]*=-1
                oldaxis[0]*=-1
                oldaxis[2]*=-1
                a=diff_angle2(oldaxis,-axxis)-pi/2.
                oldaxis=rotate(oldaxis,a,cross(oldaxis,-axxis))
                if absolute(diff_angle2(oldaxis,-axxis)-pi/2.)>.1:
                    oldaxis=rotate(oldaxis,-2.*a,cross(oldaxis,-axxis))
                axxis[0]*=-1
                axxis[2]*=-1
                pws=diff_angle2(oldaxis,rotate(vector(0,0,-1),drehwinkel,achse))
                if absolute(diff_angle2(oldaxis,rotate(rotate(vector(0,0,-1),pws,(0,1,0)),drehwinkel,achse)))<0.2:
                    winkel=winkel+pws%(2*pi)
                else:
                    winkel=winkel-pws%(2*pi)
                if len(alpha)==3:
                    alpha=[alpha[0],alpha[2]]
                while 0 in alpha:
                    alpha.remove(0)
                if alpha==[]:
                    alpha=[2*pi/3]
                for i in range(2-len(alpha)):
                    alpha.append(0)
                winkel+=pi
                pos=[pos[0]]+range(2)
                pos[1]=posn+rotate(rotate((0,-sin(alpha[0]-pi/2)*lengthB*laengen[1],cos(alpha[0]-pi/2)*lengthB*laengen[1]),winkel,(0,1,0)),drehwinkel,achse)
                if alpha[1]==0:
                    pos[2]=posn+rotate(rotate((0,-sin(alpha[0]+(2*pi-alpha[0])/2-pi/2)*lengthB*laengen[2],cos(alpha[0]+(2*pi-alpha[0])/2-pi/2)*lengthB*laengen[2]),winkel,(0,1,0)),drehwinkel,achse)
                elif alpha[1]<0:
                    pos[2]=posn+rotate(rotate((0,-sin(alpha[0]-alpha[1]-pi/2)*lengthB*laengen[2],cos(alpha[0]-alpha[1]-pi/2)*lengthB*laengen[2]),winkel,(0,1,0)),drehwinkel,achse)
                else:
                    pos[2]=posn+rotate(rotate((0,-sin(alpha[1]-pi/2)*lengthB*laengen[2],-cos(alpha[1]-pi/2)*lengthB*laengen[2]),winkel,(0,1,0)),drehwinkel,achse)
                if len(ct)==3:
                    p1=mag(ct[0]-pos[1])
                    p2=mag(ct[0]-pos[2])
                    if p1>p2:
                        if ct[1]!=ct[2]:
                            if len(konfigdic)==3:
                                p1=pos[1]
                                pos[1]=pos[2]
                                pos[2]=p1
                            else:
                                winkel+=pi
                    else:
                        if ct[1]==ct[2]:
                            if len(konfigdic)==3:
                                p1=pos[1]
                                pos[1]=pos[2]
                                pos[2]=p1
                            else:
                                winkel+=pi
                if konfigdic==[2]:
                    valenzep.append([(pos[1]-posn)/4.+posn,-2])
                else:
                    AllAtoms.append(sphere(pos=pos[1],color=atominfo2[1][0],radius=atominfo2[1][1]*sizeC+sizeCprop,opacity=opacitychosen))
                if len(konfigdic)in (1,2):
                    valenzep.append([(pos[2]-posn)/4.+posn,-2])
                else:
                    AllAtoms.append(sphere(pos=pos[2],color=atominfo2[2][0],radius=atominfo2[2][1]*sizeC+sizeCprop,opacity=opacitychosen))
        elif (len(konfigdic)==2 and sum(konfigdic)==4 or konfigdic==[3]) or valenzen==2:
                if alpha==[]:
                    alpha=[pi]
                    pos.append(0)
                if alpha[0]==0:
                    alpha[0]=pi
                pos[1]=posn+rotate((0,cos(alpha[0])*lengthB*laengen[1],sin(alpha[0])*lengthB*laengen[1]),drehwinkel,achse)
                if konfigdic==[3]:
                    valenzep.append([(pos[1]-posn)/4.+posn,-2])
                elif atominfo2[1]!=0:
                    AllAtoms.append(sphere(pos=pos[1],color=atominfo2[1][0],radius=atominfo2[1][1]*sizeC+sizeCprop,opacity=opacitychosen))
        elif len(konfigdic)==5:
                pos[1]=posn+rotate(rotate((0,-lengthB*laengen[1],0),winkel,(0,1,0)),drehwinkel,achse)
                pos[2]=posn+rotate(rotate((-lengthB*laengen[2],0,0),winkel,(0,1,0)),drehwinkel,achse)
                pos[3]=posn+rotate(rotate((lengthB*laengen[3]*cos(pi/3),0,-lengthB*laengen[3]*sin(pi/3)),winkel,(0,1,0)),drehwinkel,achse)
                pos[4]=posn+rotate(rotate((lengthB*laengen[4]*cos(pi/3),0,lengthB*laengen[4]*sin(pi/3)),winkel,(0,1,0)),drehwinkel,achse)
                AllAtoms.append(sphere(pos=pos[1],color=atominfo2[1][0],radius=atominfo2[1][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[2],color=atominfo2[2][0],radius=atominfo2[2][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[3],color=atominfo2[3][0],radius=atominfo2[3][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[4],color=atominfo2[4][0],radius=atominfo2[4][1]*sizeC+sizeCprop,opacity=opacitychosen))
        elif len(konfigdic)==6:
                pos[1]=posn+rotate(rotate((0,-lengthB*laengen[1],0),winkel,(0,1,0)),drehwinkel,achse)
                pos[2]=posn+rotate(rotate((-lengthB*laengen[2],0,0),winkel,(0,1,0)),drehwinkel,achse)
                pos[3]=posn+rotate(rotate((lengthB*laengen[3],0,0),winkel,(0,1,0)),drehwinkel,achse)
                pos[4]=posn+rotate(rotate((0,0,lengthB*laengen[4]),winkel,(0,1,0)),drehwinkel,achse)
                pos[5]=posn+rotate(rotate((0,0,-lengthB*laengen[5]),winkel,(0,1,0)),drehwinkel,achse)
                AllAtoms.append(sphere(pos=pos[1],color=atominfo2[1][0],radius=atominfo2[1][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[2],color=atominfo2[2][0],radius=atominfo2[2][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[3],color=atominfo2[3][0],radius=atominfo2[3][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[4],color=atominfo2[4][0],radius=atominfo2[4][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[5],color=atominfo2[5][0],radius=atominfo2[5][1]*sizeC+sizeCprop,opacity=opacitychosen))
        elif len(konfigdic)==7:
                pos[1]=posn+rotate(rotate((0,-lengthB*laengen[1],0),winkel,(0,1,0)),drehwinkel,achse)
                pos[2]=posn+rotate(rotate((-lengthB*laengen[2],0,0),winkel,(0,1,0)),drehwinkel,achse)
                pos[3]=posn+rotate(rotate((-cos(2*pi/5)*lengthB*laengen[3],0,-sin(2*pi/5)*lengthB*laengen[3]),winkel,(0,1,0)),drehwinkel,achse)
                pos[4]=posn+rotate(rotate((-cos(4*pi/5)*lengthB*laengen[4],0,-sin(4*pi/5)*lengthB*laengen[4]),winkel,(0,1,0)),drehwinkel,achse)
                pos[5]=posn+rotate(rotate((-cos(2*pi/5)*lengthB*laengen[5],0,sin(2*pi/5)*lengthB*laengen[5]),winkel,(0,1,0)),drehwinkel,achse)
                pos[6]=posn+rotate(rotate((-cos(4*pi/5)*lengthB*laengen[6],0,sin(4*pi/5)*lengthB*laengen[6]),winkel,(0,1,0)),drehwinkel,achse)
                AllAtoms.append(sphere(pos=pos[1],color=atominfo2[1][0],radius=atominfo2[1][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[2],color=atominfo2[2][0],radius=atominfo2[2][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[3],color=atominfo2[3][0],radius=atominfo2[3][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[4],color=atominfo2[4][0],radius=atominfo2[4][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[5],color=atominfo2[5][0],radius=atominfo2[5][1]*sizeC+sizeCprop,opacity=opacitychosen))
                AllAtoms.append(sphere(pos=pos[5],color=atominfo2[5][0],radius=atominfo2[5][1]*sizeC+sizeCprop,opacity=opacitychosen))
        ionenbindung=[]
        for i in saettigungsbeilage:
            if i==0 or "@" in i:
                ionenbindung.append(0)
                continue
            if abs(en(i)-en(natom))>2.0:
                ionenbindung.append(1)
            else:
                ionenbindung.append(0)
        if ionenbindung.count(1)>3:
            ionen=False
        else:
            ionen=True
        for i in range(len(konfigdic)):
            if saettigungsbeilage[i]!=0:
                if saettigungsbeilage[i][0]=="@":
                    s=saettigungsbeilage[i][1:]
                    while s[0] in string.digits:
                        s=s[1:]
                else:
                    s=saettigungsbeilage[i]
                valenzep.append([(pos[i]+posn)/2.,-1])
                if not (ionenbindung[i] and ionen):
                    MFB.append([AllIn.index([posn,atominfo[3]]),len(AllIn)+i,konfigdic[i],[natom,s]])
                    if MFB[-1][0]==0:
                        MFB[-1][1]+=1
                    if konfigdic[i]==2:
                        MFB[-1].append(AllAtoms[-1])
                        MFBausrichtung.append((len(MFB)-1,len(AllAtoms)-1))
        pos2=[]
        for i in range(len(saettigungsbeilage)):
            if atominfo2[i]!=0:
                pos2.append([pos[i],atominfo2[i][3]])
                if "@" in saettigungsbeilage[i][0]:
                    if "0" in saettigungsbeilage[i]:
                        i1=saettigungsbeilage[i][1:]
                        i2="x"
                        while i1[0] in digits:
                            i2+=i1[0]
                            i1=i1[1:]
                        AllIn2.append(i2)
                    else:
                        AllIn2.append("xx")
                else:
                    AllIn2.append(saettigungsbeilage[i])
                if saettigungsbeilage[i]=="H":
                    if 2.6<eval("symbol"+natom+".en"):
                        valenzep.append([pos[i],(eval("symbol"+natom+".en")-2.2)*2])
        valenzep2+=valenzep
        AllIn+=pos2
        return pos,pos2,valenzep,testebitte
def diff_angle2(x,y):
    nx=norm(x)
    ny=norm(y)
    if mag(nx+ny)>1.99:
        return 0
    elif mag(nx+ny)<0.01:
        return pi
    else:
        return diff_angle(x,y)
class smiles:
    def __init__(self,smilescode):
        self.code=smilescode
    def reduct(self):
        #löscht das erste Zeichen des SMILES-String
        self.code=self.code[1:]
    def bindung(self):
        #gibt die Bindungsinformationen aus
        b=oldcopy.copy(self.code[0])
        if self.code.startswith("-"):
            self.reduct()
            return [0,1,0]
        elif self.code.startswith("="):
            self.reduct()
            return [0,2,0]
        elif self.code.startswith("#"):
            self.reduct()
            return [0,3,0]
        else:
            return [0,1,0]
    def atom(self):
        #gibt das nächst Atom aus
        if self.code.startswith("["):
            special=True
            self.reduct()
        else:
            special=False
        symbol=oldcopy.copy(self.code[0])
        self.reduct()
        while self.code!="" and self.code[0] in letters[:26]:
            symbol+=oldcopy.copy(self.code[0])
            self.reduct()
        if special:
            while self.code[0] in ("+","-"):
                symbol+=oldcopy.copy(self.code[0])
                self.reduct()
            self.reduct()
        if self.code!="" and self.code[0] in digits:
            symbol+="*"
            while self.code!="" and self.code[0] in digits:
                symbol+=oldcopy.copy(self.code[0])
                self.reduct()
        return symbol
    def konvertiere(self):
        b=self.bindung()
        beschreibung=[self.atom(),b]
        if "*" in beschreibung[0]:
            beschreibung.append(["@"+beschreibung[0][beschreibung[0].index("*")+1:],[0,1,0]])
        while self.code.startswith("("):
            self.reduct()
            b=self.konvertiere()
            beschreibung.append(b)
        if self.code!="" and not self.code.startswith(")"):
            beschreibung.append(self.konvertiere())
        for i in range(standardvalenz(beschreibung[0],countbindungen(beschreibung))):
            beschreibung.append(["H",[0,1,0]])
        if "-" in beschreibung[0]:
            beschreibung[0]=beschreibung[0].replace("-","")
        if "+" in beschreibung[0]:
            beschreibung[0]=beschreibung[0].replace("+","")
        if self.code.startswith(")"):
            self.reduct()
        return beschreibung
    def startconvert(self):
        beschreibung=[self.atom()]
        while self.code.startswith("("):
            self.reduct()
            b=self.konvertiere()
            beschreibung.append(b)
        if self.code!="" and not self.code.startswith(")"):
            beschreibung.append(self.konvertiere())
        for i in range(standardvalenz(beschreibung[0],countbindungen(beschreibung))):
            beschreibung.append(["H",[0,1,0]])
        if "-" in beschreibung[0]:
            beschreibung[0]=beschreibung[0].replace("-","")
        if "+" in beschreibung[0]:
            beschreibung[0]=beschreibung[0].replace("+","")
        if self.code.startswith(")"):
            self.reduct()
        if "@" in str(beschreibung):
            beschreibung=cyclische(beschreibung)
        return beschreibung
def countbindungen(beschreibung):
    anzahl=0
    if type(beschreibung[1][0])==type(0):
        anzahl+=beschreibung[1][1]
    else:
        anzahl+=beschreibung[1][1][1]
    for i in beschreibung[2:]:
        anzahl+=i[1][1]
    return anzahl
def standardvalenz(x,y):
    #x=Elementsymbol, y=Anzahl bisheriger Bindungen, Doppelbindungen zaehlen doppelt, dreifachbindungen dreifach
    standvaldic={"H":[1],"B":[3],"C":[4],"N":[3,5],"O":[2],"P":[3,5],"S":[2,4,6],"F":[1],"Cl":[1],"Br":[1],"I":[1]}
    valenz={"H":1,"B":3,"C":4,"N":5,"O":6,"P":5,"S":6,"F":7,"Cl":7,"Br":7,"I":7}
    #Dictionnary mit möglichen Standardvalenzen
    #Nun wird der kleinste Wert > y gesucht
    if x not in standvaldic:
        return 0
    if "-" in x:
        wertigkeit=len(x)-x.index("-")
        x=x[:-wertigkeit]
        y-=valenz[x]+wertigkeit-8
    elif "+" in x:
        wertigkeit=len(x)-x.index("+")
        x=x[:-wertigkeit]
        y-=valenz[x]-wertigkeit-8
    for i in standvaldic[x]:
        if i<y:
            continue
        return i-y
    return 0
global bindungen
bindungen = {1:"",2:"=",3:"#",4:"$"}
def eindampfen(x):
    x = str(x)
    x = x.replace("['H', [0, 1, 3.1415926535897931]],","")
    x = x.replace("['H', [0, 1, 0]],","")
    x = x.replace(",['H', [0, 1, 3.1415926535897931]]","")
    x = x.replace(",['H', [0, 1, 0]]","")
    x = x.replace("['H', [0, 1, 3.1415926535897931]]","")
    x = x.replace("['H', [0, 1, 0]]","")
    return eval(x)

def fragmentize(x):
    global bindungen
    fernerliefen=[]
    ##fernerliefen: Sammlung der Substituenten
    SMILES_Code=""
    ##Teilcode in SMILES f?r diese Ebene
    if type(x[1][1]) == type(1) and type(x[0]) == type("a"):
        ##wenn weitere Ebene
        SMILES_Code+=bindungen[x[1][1]]+ohnezahlen(x[0])
    else:
        ##wenn erste Ebene, muss x[1] ebenfalls ausgewertet werden
        fernerliefen.append(fragmentize(x[1]))
        ##au?erdem wird das erste Atom angegeben
        SMILES_Code+=ohnezahlen(x[0])
    for i in x[2:]:
        ##Erkundung der weiteren Ebenen
        fernerliefen.append(fragmentize(i))
    ##Ordnung nach Laenge der Substituenten durch .sort()
    fernerliefen.sort()
    fernerliefen.reverse()
    ##Bis auf den letzten Substituenten werden alle in Klammern dem SMILES-Code zugefuegt
    for i in fernerliefen[:-1]:
        SMILES_Code+="("+i+")"
    if fernerliefen!=[]:
        ##Wenn es keine Substituenten gibt, mach dir keinen Stress
        SMILES_Code+=fernerliefen[-1]
        ##Der groe?te Substituent wird laut SMILES zum Schluss und ohne Klammern angehaengt
    return SMILES_Code
    ##Der Teilcode wird weiter- bzw. ausgegeben
def startconvert2(x):
    return fragmentize(eindampfen(x))
global csubs,greek1,greek2,zuckerpraefixe,bindungslaengen
csubs={"fluora":["F",1],"chlora":["Cl",1],"broma":["Br",1],"ioda":["I",1],"mercura":["Hg",2],"stanna":["Sn",4],"germa":["Ge",4],"bisma":["Bi",3],"phospha":["P",3],"selena":["Se",2],"tellura":["N",2],"arsa":["As",3],"stiba":["Sb",3],"plumba":["Pb",4],"aza":["N",3],"oxa":["O",2],"thia":["S",2],"sila":["Si",4],"aza":["N",3],"bora":["B",3],"oxonia":["O",3],"thionia":["S",3],"azonia":["N",4]}
greek1=[u'\N{GREEK SMALL LETTER ALPHA}',u'\N{GREEK SMALL LETTER BETA}',u'\N{GREEK SMALL LETTER GAMMA}',u'\N{GREEK SMALL LETTER DELTA}',u'\N{GREEK SMALL LETTER EPSILON}',u'\N{GREEK SMALL LETTER ZETA}',u'\N{GREEK SMALL LETTER ETA}',u'\N{GREEK SMALL LETTER THETA}',u'\N{GREEK SMALL LETTER IOTA}',u'\N{GREEK SMALL LETTER KAPPA}',u'\N{GREEK SMALL LETTER LAMDA}',u'\N{GREEK SMALL LETTER MU}',
u'\N{GREEK SMALL LETTER NU}',u'\N{GREEK SMALL LETTER XI}',u'\N{GREEK SMALL LETTER OMICRON}',u'\N{GREEK SMALL LETTER PI}',u'\N{GREEK SMALL LETTER RHO}',u'\N{GREEK SMALL LETTER SIGMA}',u'\N{GREEK SMALL LETTER TAU}',u'\N{GREEK SMALL LETTER UPSILON}',u'\N{GREEK SMALL LETTER PHI}',u'\N{GREEK SMALL LETTER CHI}',u'\N{GREEK SMALL LETTER PSI}',u'\N{GREEK SMALL LETTER OMEGA}']
greek2=['Alpha*', 'Beta*', 'Gamma*', 'Delta*', 'Epsilon*', 'Zeta*', 'Eta*', 'Theta*', 'Iota*', 'Kappa*','Lambda*', 'My*', 'Ny*', 'Xi*', 'Omikron*', 'Pi*', 'Rho*','Sigma*', 'Tau*', 'Ypsilon*', 'Phi*', 'Chi*', 'Psi*', 'Omega']
zuckerpraefixe={"erythr":[{2:1,3:1},4],"thre":[{2:-1,3:1},4],"rib":[{2:1,3:1,4:1},5],"arabin":[{2:-1,3:1,4:1},5],"xyl":[{2:1,3:-1,4:1},5],"lyx":[{2:-1,3:-1,4:1},5],"desoxyrib":[{3:1,4:1},5],"all":[{2:1,3:1,4:1,5:1},6],"altr":[{2:-1,3:1,4:1,5:1},6],"tal":[{2:-1,3:-1,4:-1,5:1},6],"gluc":[{2:1,3:-1,4:1,5:1},6],"gul":[{2:1,3:1,4:-1,5:1},6],"mann":[{2:-1,3:-1,4:1,5:1},6],"galact":[{2:1,3:-1,4:-1,5:1},6],"id":[{2:-1,3:1,4:-1,5:1},6]}
bindungslaengen={"C":{"C":1}}
def analyse(x):
    global csubs,snl,zuckerpraefixe,greek1,cyc,greek2,snl,mi,praelist,fuell,fehlerapp,cyc2
    cyc2=0
    snl=[]
    praelist=[]
    fuell=[]
    cyc=0
    #x=zu analysierender Name
    ausgabe=[0,[],[]]
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
            ausgabe.append("?")
            x=lower(row[1])+x
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
                        ausgabe.append([temp_hwp[1][i],coefi[-1][i],trivialsdazu])
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
def coefiwahl(coefi,anzahl,trivials):
    for i in range(len(coefi)-1,-1,-1):
        if len(coefi[i])==anzahl:
            return coefi[i],coefi[:i]+coefi[i+1:],trivials
    if not "per" in trivials and not "o(" in trivials:
        trivials.append("coeftest")
    return range(1,anzahl+1),coefi,trivials
def esterkompetenz(temp,ausgabe):
    if temp[0]:
        if len(temp[0][-1])==3:
            temp[1]=temp[0][-1][1][1]
            ausgabe.append([[ncalkan(temp[0][-1][0][0]),{1:["yl"]},["coeftest"]],1])
            temp[0]=temp[0][:-1]
            if temp[1]=="":
                temp[1]="-"
    return temp,ausgabe
def boesewoerter(ausgabe):
    i=0
    boeses=[]
    while i<len(ausgabe):
        if boesesequenz(ausgabe[i:]):
            boese=""
            while i<len(ausgabe) and boeseszeichen(ausgabe[i]):
                boese+=ausgabe[i]
                del ausgabe[i]
            boeses.append(boese)

        i+=1
    return boeses,ausgabe
def boesesequenz(x):
    if len(x)<3:
        return False
    if boeseszeichen(x[0])and boeseszeichen(x[1])and boeseszeichen(x[2]):
        return True
def boeseszeichen(x):
    if type(x)==str and x not in (" ","-","",","):
        return True
def anorganisch(ausgabe2):
    suffixlist=[]
    praelist=[]
    for i in ausgabe2:
        i3=upper(i[0][0])+i[0][1:]
        if "suffix" in i and i3 not in namen:
            suffixlist.append(eval(suffix[i[0]]))
        elif type(i)!=type("a"):
            if i3 in namen:
                stoff=[name[i3]]
                if stoff in ("Lithium","Natrium","Kalium","Rubidium","Caesium"):
                    stoff.append([0,1,0])
                elif stoff in ("Beryllium","Magnesium","Calcium","Strontium","Barium"):
                    stoff.sppend([0,2,0])
                elif stoff in ("Fluor","Chlor","Brom","Iod"):
                    stoff.append([0,1,0])
                elif stoff in ("Sauerstoff","Schwefel","Selen","Tellur"):
                    stoff.append([0,2,0])
                else:
                    stoff.append([0,1,0])
                praelist.append(stoff)

            else:
                praelist.append(praefix[i[0]])
    if len(suffixlist)==1:
        suffix1=plusweg(suffixlist[0])
        for i in praelist:
            suffix1.append(i)
        return suffix1
    else:
        praefix1=praelist[0]
        del praefix1[1]
        for i in suffixlist:
            bindung=[0,i.count("+"),0]
            i2=plusweg(i)
            i2.insert(1,bindung)
            praefix1.append(i2)
        return praefix1
def plusweg(x):
    for i in range(len(x)):
        if i>len(x)-1:
            break
        if x[i]=="+":
            del x[i]
    return x
def orstartswith(x,arg):
    for i in arg:
        if x.startswith(i):
            return True
def hauptgruppe(i):
    if len(i)==2 and (len(i[0])==3 or (len(i[0])>3 and "trivial" in i[0][2])):
        return True
def ausgabeordner(ausgabe2,umfang=False,klammer=False):
    global snl,praelist,csubs,fuell
    last2=""
    ausgabes=[0,0,0]
    if ausgabe2[0]==0:
        ausgabes=ausgabe2[:3]
        ausgabe2=ausgabe2[3:]
    if not "{" in str(ausgabe2):
        return anorganisch(ausgabe2),False
    while ausgabe2!=[]:
        i=ausgabe2[0]
        if type(i)==type("-"):
            fuell+=i
            ausgabe2=ausgabe2[1:]
            continue
        else:
            fuell=[]
        last=last2
        last2=ausgabe2[0]
        ausgabe2=ausgabe2[1:]
        if len(i)==2 and len(i[0])==2:
            continue
        if len(i)==3 and i[0] in csubs.keys():
            ausgabes.append(i)
            continue
        if len(i)==4 and "suffix" in i:
            i.remove("suffix")
            if "(" in i[0]:
                psyn=[name[i[0][:i[0].index("(")].capitalize()]]
                for i in range(sfrw(i[0][i[0].index("("):])):
                    psyn.append('+')
                psyn=str(psyn)
                psyn=psyn.replace("'",'"')
            else:
                psyn=info("suffix",i[0])
            bindungen=[psyn.count('"+"'),psyn.count('"++"'),psyn.count('"+++"')]
            ausgabeteil=i
            while sum(bindungen)>1:
                if praelist+ausgabe2[1:]==[]:
                    praelist.append([["hydro",0,[]],1])
                for i1 in praelist+ausgabe2[1:]:
                    if praelist==[]:
                        praeleer=True
                    else:
                        praeleer=False
                    if len(i1)==4:
                        if not praeleer:
                            continue
                        a=ausgabeordner(ausgabe2,True)
                        ausgabe2=a[1]
                        ausgabeteil.append(a[0])
                        b=ausgabeteil[-1][1]
                    elif len(i1)==3:
                        continue
                    elif len(i1)==2 and (len(i1[0])==3 or (len(i1[0])>3 and "trivial" in i1[0][2])):
                        if praeleer:
                            a=ausgabeordner(ausgabe2,True)
                            ausgabe2=a[1]
                            ausgabeteil.append(a[0])
                        else:
                            ausgabeteil.append(i)
                        b=1
                    if b>0:
                        if bindungen[b-1]>0:
                            bindungen[b-1]-=1
                        else:
                            if b==1 and bindungen[1]>0:
                                if bindungen[1]>0:
                                    bindungen[1]-=1
                                    bindungen[2]=1
                            elif (b==2 or b==3) and bindungen[1]>1:
                                bindungen[0]-=b
                            elif b==2 or (b==1 and bindungen[1]==0):
                                bindungen[2]-=1
                                bindungen[b-1]+=3-b
                    ausgabe2=ausgabe2[1:]
            psyn2=summenformel2(eval(psyn))
            if "H" in psyn2.keys():
                potenziell1=psyn2["H"]
            else:
                potenziell1=0
            psynlist={}
            for i2 in ausgabe2:
                if type(i2)==type("-"):
                        continue
                if i2[1] in psyn2:
                    if i2[1] not in psynlist.keys():
                        psynlist[i2[1]]=potenziell(psyn,i2[1])
                    if psynlist[i2[1]]==0:
                        continue
                    ausgabeteil=dazu2(ausgabeteil,i2)
                    ausgabe2=ausgabe2[1:]
                    psynlist[i2[1]]-=1
                    potenziell1-=1
            if potenziell1>0:
                oldpraelist=oldcopy.copy(praelist)
                for i2 in oldpraelist:
                    if hauptgruppe(i2) and "coeftest" in i2[0][2]:
                        ausgabeteil=dazu2(ausgabeteil,i2)
                        praelist.remove(i2)
                        potenziell1-=1
                        if potenziell1==0:
                            break
            if potenziell1>0:
                for i2 in ausgabe2:
                    if hauptgruppe(i2) and "coeftest" in i2[0][2]:
                        ausgabeteil=dazu2(ausgabeteil,i2)
                        ausgabe2=ausgabe2[1:]
                        potenziell1-=1
                        if potenziell1==0:
                            break
            if not klammer:
                praelist.append(ausgabeteil)
                continue
        elif len(i)==3:
            ausgabeteil=i
            if not vergleich(i,last,ausgabe2):
                psyn=info("praefix",i[0])
                psyn2=summenformel2(eval(psyn))
                if "H" in psyn2.keys():
                    potenziell1=psyn2["H"]
                    if eval(psyn)[0]=="H":
                        potenziell1-=1
                else:
                    potenziell1=0
                psynlist={}
                for i2 in ausgabe2:
                    if type(i2)==type("-"):
                        continue
                    if i2[1] in psyn2:
                        if i2[1] not in psynlist.keys():
                            psynlist[i2[1]]=potenziell(psyn,i2[1])
                        if psynlist[i2[1]]==0:
                            continue
                        ausgabeteil=dazu2(ausgabeteil,i2)
                        ausgabe2=ausgabe2[1:]
                        psynlist[i2[1]]-=1
                        potenziell1-=1
                if potenziell1>0:
                    for i2 in ausgabe2:
                        if len(i2)==2 and fuell==[] and "coeftest" in ausgabeteil[2]:
                            ausgabeteil[1]=i2[1]
                            i2[1]=1
                            i2[0][2].append("coeftest")
                            ausgabeteil[2].remove("coeftest")
                            ausgabeteil=dazu2(ausgabeteil,i2)
                            ausgabe2=ausgabe2[1:]
                            potenziell1-=1
                            if potenziell1==0:
                                break
                        else:
                            break
        elif hauptgruppe(i):
            ylstelle=1
            ausgabeteil=i
            radikal2=[]
            radikal=False
            for i1 in i[0][1].keys():
                for i2 in ("ylen","ylin","yliden","ylidin","yl","oyl","oxy","azo","o(","azano","azeno"):
                    if i2 in i[0][1][i1]:
                        radikal=True
                        radikal2.append(i2)
            if "bi" in i[0][2] or "poly" in i[0][2]:
                radikal=False
            if vergleich(i,last,ausgabe2) and radikal2.count("ylen")+radikal2.count("ylin")==len(radikal2):
                if not radikal:
                    ausgabeteil[0][1]=dazu("yl",analysezusyntax(i,check=True),ausgabeteil[0][1])
                if not klammer:
                    praelist.append(ausgabeteil)
                continue
            elif  radikal:
                if praelist!=[]:
                    yls=0
                    ylens=0
                    ylins=0
                    for i2 in i[0][1].keys():
                        if "yl" in i[0][1][i2]:
                            yls+=1
                        elif "yliden" in i[0][1][i2]:
                            ylens+=1
                        elif "ylidin" in i[0][1][i2]:
                            ylins+=1
                    for i2 in praelist:
                        if yls+ylens+ylins==0:
                            break
                        if "suffix" in i2:
                            i2.remove("suffix")
                        b=1
                        b=["yls","ylens","ylins"][b-1]
                        if eval(b)==0:
                            continue
                        exec(b+"-=1")
                        for i3 in i[0][1].keys():
                            if b[:-1] in i[0][1][i3]:
                                i[0][1][i3].remove(b[:-1])
                                if i[0][1][i3]==[]:
                                    del i[0][1][i3]
                                    radikal=False
                                    i2[1]=i3
                                    if "coeftest" in i2[2]:
                                        i2[2].remove("coeftest")
                                    i[0][1]=dazu("an",1,i[0][1])
                                    break
                                if not radikaltester(i[0][1]):
                                    radikal=False
                                    i[0][1]=dazu("an",1,i[0][1])
                        praelist=praelist[1:]
                        ausgabeteil[0].append(i2)
                fuell2=[]
                if not "o(" in str(ausgabeteil[0][1]) and not "poly" in ausgabeteil[0][2]:
                    while ausgabe2!=[]:
                        i2=ausgabe2[0]
                        if type(i2)==type("-"):
                            fuell2+="-"
                            ausgabe2=ausgabe2[1:]
                            continue
                        if ausgabe2!=[] and len(ausgabe2[0])==2:
                            break
                        if len(i2)==2 and len(i2[0])==2:
                            if i2[0]==ausgabe2[0] and i2[1]==ausgabe2[1]+1:
                                break
                        elif hauptgruppe(i2):
                            if not "coeftest" in i2[0][2] or fuell2!=[]:
                                break
                        elif len(i2)==3:
                            if fuell+fuell2!=[] and not "coeftest" in i2[2]:
                                break
                            if not "coeftest" in i2[2] and "coeftest" in ausgabeteil[0][2]:
                                ausgabeteil[1]=i2[1]
                                ausgabeteil[0][2].remove("coeftest")
                                i2[1]=1
                                i2[2].append("coeftest")
                        ausgabeteil[0].append(i2)
                        ausgabe2=ausgabe2[1:]
                    if not radikal:
                        for i2 in ausgabeteil[2:]:
                            ausgabes.append(i2)
                        for i2 in ausgabeteil[0][3:]:
                            ausgabes.append(i2)
                        ausgabes[:3]=ausgabeteil[0][:3]
                        for i in praelist:
                            ausgabes.append(i)
                        praelist=[]
                        continue
            else:
                ausgabe1=ausgabes[2]
                for i2 in ausgabeteil[0][3:]:
                    ausgabes.append(i2)
                ausgabes[:3]=ausgabeteil[0][:3]
                if ausgabe1:
                    ausgabes[2]+=ausgabe1
                for i in praelist:
                    ausgabes.append(i)
                praelist=[]
                continue
            if ausgabes[0]==0 and not klammer:
                praelist.append(ausgabeteil)
                ausgabe2=ausgabe2[1:]
                continue
        else:
            ausgabeteil=i
            ausgabeteil=[[ausgabeteil[0][:3],ausgabeteil[1]]]+ausgabeteil[0][3:]
            ausgabeteil=ausgabeordner(ausgabeteil,klammer=True)
            if type(ausgabeteil[0])==int:
                return ausgabeteil
            ausgabeteil[0]+=ausgabeteil[2:]
            del ausgabeteil[2:]
        if umfang:
            return ausgabe2,ausgabeteil
        if klammer and ausgabes[0]==0:
            klammer=False
            for i2 in ausgabeteil[0][3:]:
                ausgabes.append(i2)
            ausgabes[:3]=ausgabeteil[:3]
        else:
            ausgabes.append(ausgabeteil)
    if praelist!=[]:
        if ausgabes[0]==0:
            ausgabe1=ausgabes[2]
            if len(praelist[-1])==2:
                for i2 in praelist[-1][0][3:]:
                    ausgabes.append(i2)
                ausgabes[:3]=praelist[-1][0][:3]
            else:
                for i2 in praelist[-1][3:]:
                    ausgabes.append(i2)
                ausgabes[:3]=praelist[-1][:3]
            ausgabes[2]+=ausgabe1
            praelist=praelist[1:]
        ausgabes+=praelist
    if type(ausgabes[0])==int:
        if "zucker" in str(ausgabes[1]):
            for i in ausgabes[3:]:
                if len(i)==2:
                    if "zucker" in str(i[0][1]):
                        zuckerstelle=i[1]
                        for i2 in range(3,len(ausgabes)):
                            if ausgabes[i2][0]=="hydroxy":
                                if ausgabes[i2][1]==zuckerstelle:
                                    del ausgabes[i2]
                                    break
                        break
    if type(ausgabes[0])==list:
        for i2 in range(len(ausgabes[0][2])):
            if type(ausgabes[0][2][i2])==list:
                for i in range(len(ausgabes[0][2])):
                    if ausgabes[0][2][i] in ("(s)","(r)"):
                        ausgabes[0][2][i]=str([ausgabes[0][2][i],ausgabes[0][2][i2].pop(0)])
                del ausgabes[0][2][i2]
                break
    elif type(ausgabes[0])==int:
        for i2 in range(len(ausgabes[2])):
            if type(ausgabes[2][i2])==list:
                for i in range(len(ausgabes[2])):
                    if ausgabes[2][i] in ("(s)","(r)"):
                        ausgabes[2][i]=str([ausgabes[2][i],ausgabes[2][i2].pop(0)])
                del ausgabes[2][i2]
                break
    ausgabes=cycloreparierer(ausgabes,False)
    ausgabes=induzierregler(ausgabes,False)
    for i in ausgabes[3:]:
        if len(i)==2:
            for i1 in i[0][1].keys():
                if "o(" in i[0][1][i1]:
                    for i2 in range(len(ausgabes)-3):
                        if ausgabes[i2+3]==i or type(ausgabes[i2+3])==str:
                            continue
                        lokant=oldcopy.copy(ausgabes[i2+3][1])+i1
                        if lokant>ausgabes[0]-1:
                            ausgabes[i2+3][1]=i[0][0]-(lokant-ausgabes[0]+1)
                            i[0].append(ausgabes[i2+3])
                            ausgabes[i2+3]="-"
                        else:
                            ausgabes[i2+3][1]=lokant%ausgabes[0]+1
                    neuesendungsdictionary={}
                    neuesendungsdictionary2={}
                    for i2 in ausgabes[1].keys():
                        if "en" in ausgabes[1][i2]:
                            neuesendungsdictionary2[i2]="en"
                            ausgabes[1][i2].remove("en")
                        elif "in" in ausgabes[1][i2]:
                            neuesendungsdictionary2[i2]="in"
                            ausgabes[1][i2].remove("in")
                        neuesendungsdictionary[(i2+i1-1)%ausgabes[0]]=ausgabes[1][i2]
                    for i2 in neuesendungsdictionary:
                        if i2>ausgabes[0]-2:
                            for i3 in neuesendungsdictionary[i2]:
                                i[0][1]=dazu(i3,i2-ausgabes[0]+3,i[0][1])
                    for i2 in neuesendungsdictionary2:
                        neuesendungsdictionary=dazu(neuesendungsdictionary2[i2],i2,neuesendungsdictionary)
                    ausgabes[1]=neuesendungsdictionary
                    break
    return ausgabes
def induzierregler(ausgabes,klammer):
    if klammer:
        for i in ausgabes[0][3:]:
            if type(i[0])==type([2, {1: ['yl']}, [], ['hydroxy', 2, []]]):
                i=cycloreparierer(i,True)
                h=Hholer(i[0][2])
                if h:
                    h,i[0][2]=h
            elif type(i)==type(["oxa",4,["H4"]]):
                h=Hholer(i[2])
                if h:
                    h,i[2]=h
            else:
                continue
            if h and "cyclo" in ausgabes[0][2]:
                ausgabes[0][1]=enSchubser(ausgabes[0][1],h)
    else:
        ausgabes=[ausgabes,1]
        ausgabes=induzierregler(ausgabes,True)[0]
    return ausgabes
def enSchubser(x1,ind):
    for i in x1:
        if ind>i:
            continue
        if ind+2==i:
            break
        if "en" in x1[i]:
            x1[i].remove("en")
            x1=enSchubser(x1,i)
            x1=dazu("en",i+1,x1)
            break
    return x1
def Hholer(x2):
    for i in x2:
        if type(i)not in (str,unicode):
            continue
        if i[0]=="H":
            x2.remove(i)
            return eval(i[1:]),x2
def cycloreparierer(ausgabes,klammer):
    if klammer:
        for i in ausgabes[0][3:]:
            if type(i[0])==type([2, {1: ['yl']}, [], ['hydroxy', 2, []]]):
                if "cyclo" in i[0][2]:
                        ylstelle=0
                        for i3 in i[0][1].keys():
                            for i2 in ("ylen","ylin","yliden","ylidin","yl","oyl","oxy","azo","azano","azeno"):
                                if i2 in i[0][1][i3]:
                                    i[0][1][i3].remove(i2)
                                    i[0][1][i3]+=["eigentlichyl"]
                                    i[0][1]=dazu(i2,1,i[0][1])
                                    ylstelle=i3
                        if ylstelle!=0:
                            for i3 in range(3,len(i[0])):
                                if type(i[0][i3])==str:
                                    continue
                                i[0][i3][1]=(i[0][i3][1]-ylstelle)%i[0][0]+1
                            for i3 in range(len(i[0][2])):
                                if i[0][2][i3][0]=="[":
                                    i[0][2][i3]=eval(i[0][2][i3])
                                    i[0][2][i3][1]=(i[0][2][i3][1]-ylstelle)%i[0][0]+1
                                    i[0][2][i3]=str(i[0][2][i3])
                i=cycloreparierer(i,True)
    else:
        ausgabes=[ausgabes,1]
        ausgabes=cycloreparierer(ausgabes,True)[0]
    return ausgabes
def radikaltester(x):
    if type(x)==type([]):
        for ii in ("ylen","ylin","yliden","ylidin","yl","oyl","oxy","azo","o(","azano","azeno"):
            if ii in x:
                return True
    elif type(x)==type({}):
        for ii in ("ylen","ylin","yliden","ylidin","yl","oyl","oxy","azo","o(","azano","azeno"):
            for iii in x.keys():
                if ii in x[iii]:
                    return True
    return False
def vergleich(x,y,z):
    if (y=="" or len(y)!=len(x)) and (z==[] or len(z[0])!=len(x)):
        return False
    if y=="" or len(y)!=len(x):
        if len(x) in (3,4):
            if x[0]==z[0][0] and x[2]==z[0][2]:
                return True
        elif len(x)==2:
            if x[0]==z[0][0]:
                return True
    elif z==[] or len(z[0])!=len(x):
        if len(x) in (3,4):
            if (x[0]==y[0] and x[2]==y[2]):
                return True
        elif len(x)==2:
            if x[0]==y[0]:
                return True
    elif len(x) in (3,4):
        if (x[0]==y[0] and x[2]==y[2]) or (x[0]==z[0][0] and x[2]==z[0][2]):
            return True
    elif len(x)==2:
        if x[0]==y[0] or x[0]==z[0][0]:
            return True
    return False
def dazu2(ausgabe4,x):
    if len(ausgabe4)==2:
        ausgabe4=[ausgabe4,x]
    else:
        ausgabe4.append(x)
    return ausgabe4
def summenformel(x):
    f=[ohnezahlen(x[0])]
    for i in x[1:]:
        if type(i[0]) in (type(1.9),type(1)):
            continue
        if "@" in i[0]:
            continue
        f+=summenformel(i)
    return f
def potenziell(x,y):
    p=0
    if x[0]==y:
        beding=True
    else:
        beding=False
    for i in x[1:]:
        if type(i[0])==type(1):
            continue
        if i[0]=="H":
            p+=1
        else:
            p+=potenziell(i,y)
    return p
def summenformel2(x):
    sf={}
    x=summenformel(x)
    for i in name.values():
        if i in x:
            sf[i]=x.count(i)
    return sf
def suffixanstamm(ausgabe,coefi):
    ausgabe2=ausgabe[3:]
    ausgabe2.reverse()
    for i in ausgabe2:
        if len(i)==2:
            if i[1]==1:
                i2=0
                for i1 in i[0][1].keys():
                    if "yl" in i[0][1][i1]:
                        substelle=i1
                        i[0][1][i1].remove("yl")
                        if i[0][1][i1]==[]:
                            del i[0][1][i1]
                        i2+=1
                        if i2>=len(coefi):
                            break
            else:
                substelle=i[1]
            ausgabe2.reverse()
            if type(ausgabe[0])==type(1):
                ausgabe[1]=dazu("yl",i[1],ausgabe[1])
                ausgabe3=[[ausgabe[0],ausgabe[1],ausgabe[3]],0]
            else:
                ausgabe3=[ausgabe[0],0,ausgabe[2]]
            if coefi!=[]:
                for i1 in coefi:
                    ausgabe3[1]=i1
                    ausgabe2.append(ausgabe3)
            else:
                ausgabe3[1]=substelle
                ausgabe2.append(ausgabe[3])
            ausgabe2=i[0][0:3]+ausgabe2
            ausgabe2.remove(i)
            if len(i[0])>3:
                ausgabe2.append(i[0][3:])
            ausgabe=ausgabe2
            return ausgabe,coefi
def analysezusyntax(x,check=False,endzusatz={}):
    global cis,trans,csubs,mi,annelierungswinkel,fehlerapp,cyc2
    if len(x)==2 and x[1]==False:
        return x[0]
    if type(x[0])==type("chlor") and x[1]!=[0]:
        if x[0] in csubs:
            syntax=csubs[x[0]]
            for i in x[2]:
                if i.startswith("lambda"):
                    syntax[1]=eval(i[7:-1])
        elif praes(x[0])[1]=="":
            syntax=eval(info("praefix",x[0]))
        else:
            syntax=info("suffix",x[0])
            if '"+"' in syntax:
                b='"+"'
            elif '"++"' in syntax:
                b='"++"'
            else:
                b='"+++"'
            h=syntax.index(b)
            syntax=Chiralitaetszentrenordner(eval(syntax[:h]+"['C*',[0,"+str(b.count("+"))+",0]]"+syntax[len(b)+h:]))[1]
        per=0
        lr=0
        if "per" in x[2]:
            per=1
        if "(s)" in x[2]:
            lr="links"
        elif "(r)" in x[2]:
            lr="rechts"
        if "(z)" in x[2]:
            syntax[1][2]="cis"+str(cis/2)
            cis+=1
        elif "(e)" in x[2]:
            syntax[1][2]="trans"+str(trans/2)
            trans+=1
        if len(x)>3:
            for i in x[3:]:
                syntax2=analysezusyntax(i)[1]
                syntax=substituiere(syntax,syntax2)
        if 1 in x[2]:
            syntax[1].append("1")
        elif -1 in x[2]:
            syntax[1].append("0")
        return [x[1],syntax,per,lr,[]]
    else:
        if x[0]==0:
            if len(x)>3:
                x=analysezusyntax(x[3])
                return x
            else:
                showinfo(title="Fehler",message="Aus dem vorliegenden Namen konnte kein IUPAC-Name analysiert werden.\nEventuell liegt ein Rechtschreib- oder Klammerungsfehler vor.\nIst das nicht der Fall, mÃ¼ssen eventuell PrÃ¤fixe, Suffixe oder Trivialnamen zur Datenbank hinzugefÃ¼gt werden")
                6/0
        per=["H",[0,1,0]]
        substituenten={}
        if type(x[1])==type(1) or (type(x[1])==type("4'") and x[1][0] in digits) or (x[1] in atomlist.keys()):
            stelle=x[1]
            x=x[0]
        else:
            stelle=0
        triarg={}
        triarghelp={}
        chzentren=[]
        coeftestwuerdig=[]
        amidaminolist=[]
        multiplikation=[]
        if "bi" in x[2]:
            multiplikation=[[1,1,0]]
            b1=False
            b2=False
            for i in x[1].keys():
                if "yl" in x[1][i]:
                    if type(i)==type(1) and not b1:
                        multiplikation[0][0]=i
                        b1=True
                        x[1][i].remove("yl")
                        if x[1][i]==[]:
                            del x[1][i]
                    elif not b2:
                        multiplikation[0][1]=i
                        b2=True
                        x[1][i].remove("yl")
                        if x[1][i]==[]:
                            del x[1][i]
            x[2].remove("bi")
        zentral=["C",4]
        erstes_polymerende=["H",[0,1,0]]
        zweites_polymerende=["H",[0,1,0]]
        Hsammler=[]
        Hsammlerzahl=0
        encount=0
        nochdran=[]
        for i in x[2]:
            if type(i)==str:
                if i.startswith("H"):
                    Hsammler.append(eval(i[1:]))
                elif i.startswith("spiro"):
                    zahlen=i[6:-1].split(".")
                    zahlen=[eval(zahlen[0]),eval(zahlen[1])]
                    cyclo=1
                    substituenten[zahlen[0]]=[["@1C",[0,1,0]]]
                    nochdran=[zahlen[0],zahlen[0]+1,{},{0:"*"}]
                    x[0]=zahlen[0]
        if x[1]!=0:
            secarg={}
            oka=False
            for i in x[1].keys():
                for a in x[1][i]:
                    if a=="o(":
                        for i3 in (i-1,i):
                            if i3 in endzusatz:
                                oka=True
            Endungslokantenfehler=[]
            for i in x[1].keys():
                    for a in x[1][i]:
                        if i>x[0]-1 and a in ("en","in"):
                            Endungslokantenfehler.append("'"+a+"'")
                            x[1][i].remove(a)
                            continue
                        if i in Hsammler:
                            Hsammlerzahl+=1
                        if a in ("azen","en","azeno") and not "o(" in a:
                            encount2=0
                            cistrans=0
                            for i2 in x[2]:
                                if i2 in ("(z)","(e)"):
                                    i2={"(e)":"trans","(z)":"cis"}[i2]
                                    if encount2==encount:
                                        cistrans=i2+str(eval(i2)/2)
                                        exec(i2+"+=1")
                                        break
                                    encount2+=1
                            if oka:
                                secarg.__init__({i+1+Hsammlerzahl:[0,2,cistrans]})
                            else:
                                secarg.__init__({i+Hsammlerzahl:[0,2,cistrans]})
                            encount+=1
                        if "in" == a:
                            secarg.__init__({i:[0,3,0,0]})
                            if a in Hsammler:
                                Hsammlerzahl+=1
                            if oka:
                                secarg.__init__({i+1+Hsammlerzahl:[0,3,0,0]})
                            else:
                                secarg.__init__({i+Hsammlerzahl:[0,3,0,0]})
        for i in range(3,len(x)):
            if type(x[i])==str:
                continue
            if "poly" in x[2]:
                if x[i][1]==2 and ((type(x[0])==str and "greek" in x[i][2]) or type(x[0])==list and "greek" in x[i][0][2]):
                    if len(x[i])==2:
                        erstes_polymerende=analysezusyntax(x[i][0])[1]
                    else:
                        erstes_polymerende=analysezusyntax(x[i])[1]
                    continue
                if x[i][1]==25 and ((type(x[0])==str and "greek" in x[i][2]) or type(x[0])==list and "greek" in x[i][0][2]):
                    if len(x[i])==2:
                        zweites_polymerende=analysezusyntax(x[i][0])[1]
                    else:
                        zweites_polymerende=analysezusyntax(x[i])[1]
                    continue
            if type(x[i][0][0])==type(1) and not "yl" in str(x[i][0][1])  and not "oyl" in str(x[i][0][1]) and not "oxy" in str(x[i][0][1]) and not "azo" in str(x[i][0][1]) and not "o(" in str(x[i][0][1]) and not "azano" in str(x[i][0][1])and not "azeno" in str(x[i][0][1]):
                continue
            if type(x[i][0][0])==type(1):
                if "coeftest" in x[i][0][2] and not "n*-" in x[i][0][2]:
                    x[i][0][2]=x[i][0][2][:x[i][0][2].index("coeftest")]+x[i][0][2][x[i][0][2].index("coeftest")+1:]
                    coeftestwuerdig.append(i)
                    continue
            else:
                if "coeftest" in x[i][2] and not "n*-" in x[i][2]:
                    x[i][2]=x[i][2][:x[i][2].index("coeftest")]+x[i][2][x[i][2].index("coeftest")+1:]
                    coeftestwuerdig.append(i)
                    continue
            a=analysezusyntax(x[i],endzusatz=secarg)
            if type(a[0])==type("a") and a[0][0] not in digits:
                return a
            if "+" in str(a[1]):
                multiplikation+=[[a[0],1,a[1]]]
                continue
            if type(a[1][1])==type(1):
                triarg.__init__({a[0]:a[1]})
            else:
                if a[4]!=[]:
                    a[0]=a[4][0][0]
                    substituenten=dazu(["@0"+a[4][0][2]+a[4][0][1],[-annelierungsbindung,1,0]],a[0],substituenten)
                    a[1]=a[1][2]
                    a[1][1][0]=annelierungsbindung
                    a[0]=(a[0])%x[0]+1
                    a[1][1][2]=10*pi
                if a[2]!=0:
                    per=a[1]
                else:
                    h=1
                    if type(x[i][0][0])==type(1):
                        if "n*-" in x[i][0][2]:
                            amidaminolist.append(a)
                            h=0
                    else:
                        if "n*-" in x[i][2]:
                            amidaminolist.append(a)
                            h=0
                    if h==1:
                        substituenten=dazu(a[1],a[0],substituenten)
            if a[3]!=0:
                chzentren.append([a[0],a[3]])
        if x[1]!=[0]:
            ylstelle=0
            ylstelle2=1
            ylstelle3=0
            oklatur=[]
            lweg=False
            if "per" in x[2]:
                per2=1
            else:
                per2=0
            if "cyclo" in x[2]:
                cyclo=1
            else:
                cyclo=0
            lr=0
            if "(s)" in x[2]:
                lr="links"
            elif "(r)" in x[2]:
                lr="rechts"
            bruecke=""
            oka=False
            if 0 in secarg.keys():
                del secarg[0]
            for i in x[1].keys():
                if i not in (x[0],1) or "cyclo" in x[2] or "bicyclo" in x[2]:
                    carbo=True
                else:
                    carbo=False
                for a2 in range(len(x[1][i])):
                    a=x[1][i][a2]
                    if a not in ("sil","silaz","silox","azan","azen","german","stann","plumb","stib"):
                        if type(i)!=str and i>x[0]:
                            Endungslokantenfehler.append("'"+a+"'")
                            continue
                    if a in ("oat","at"):
                        if i in substituenten:
                            a2=substituenten[i][-1]
                            del substituenten[i][-1]
                        elif coeftestwuerdig!=[]:
                             a2=analysezusyntax(x[coeftestwuerdig[0]])[1]
                             coeftestwuerdig=coeftestwuerdig[1:]
                        elif 1 in substituenten:
                            a2=substituenten[1][-1]
                            del substituenten[1][-1]
                        else:
                            a2=False
                        if carbo:
                            if a2:
                                substituenten=dazu(["C",[0,1,0],["O",[0,2,0]],["O",[0,1,0],a2]],i,substituenten)
                            else:
                                substituenten=dazu(["C",[0,1,0],["O",[0,2,0]],["O",[0,1,0]]],i,substituenten)
                        else:
                            if a2:
                                substituenten=dazu(["O",[0,1,0],a2],i,substituenten)
                            else:
                                substituenten=dazu(["O",[0,1,0]],i,substituenten)
                            substituenten[i].append(["O",[0,2,0]])
                    if "sultam"==a:
                        cyclo=1
                        nochdran=[i,x[0]-i,{i+2:[["O",[0,2,0]],["O",[0,2,0]]]},{i+1:["N",3],i+2:["S",6]}]
                        #nochdran = [ Koefizient, ab dem alle Substituenten umgeleitet werden müssen
                        #             ; Laenge der Verlaengerung
                        #             ; Substituentenausnahmen in Substituentenstruktur, Ausgetauschte
                        #             ; in Austauschstruktur]
                        x[0]=i+2
                    if "lactam"==a:
                        cyclo=1
                        substituenten=dazu(["O",[0,2,0]],1,substituenten)
                        nochdran=[i,x[0]-i,{},{i+1:["N",3]}]
                        x[0]=i+1
                    if "sulton"==a:
                        cyclo=1
                        nochdran=[i,x[0]-i,{i+2:[["O",[0,2,0]],["O",[0,2,0]]]},{i+1:["O",3],i+2:["S",6]}]
                        x[0]=i+2
                    if a in ("olid","lacton"):
                        if i==1:
                            i2=x[0]
                        else:
                            i2=oldcopy.copy(i)
                        cyclo=1
                        substituenten=dazu(["O",[0,2,0]],1,substituenten)
                        nochdran=[i2,x[0]-i2,{},{i2+1:["O",2]}]
                        x[0]=i2+1
                    if "sil" == a:
                        zentral=["Si",4]
                    if "german" == a:
                        zentral=["Ge",4]
                    if "stann" == a:
                        zentral=["Sn",4]
                    if "plumb" == a:
                        zentral=["Pb",4]
                    if "stib" == a:
                        zentral=["Sb",3]
                    if "silaz" == a:
                        zentral=["Si",4]
                        x[0]+=x[0]-1
                        for i in range(2,x[0],2):
                            triarg[i]=["N",3]
                        if "cyclo" in x[2]:
                            x[0]+=1
                            triarg[x[0]]=["N",3]
                    if "silox" == a:
                        zentral=["Si",4]
                        x[0]+=x[0]-1
                        for i in range(2,x[0],2):
                            triarg[i]=["O",2]
                        if "cyclo" in x[2]:
                            x[0]+=1
                            triarg[x[0]]=["O",2]
                    if a in ("azan","azen"):
                        zentral=["N",3]
                    if a in ("azano","azeno"):
                        zentral=["N",3]
                        ylstelle=1
                        ylbindung=[0,1,0]
                    if "oxy" == a:
                        ylstelle=i
                        ylbindung=[0,1,0]
                        bruecke=bruecken(bruecke,"['O',[0,1,0],+]")
                    if "methoxy" == a:
                        ylstelle=i
                        ylbindung=[0,1,0]
                        bruecke=bruecken(bruecke,"['O',[0,1,0],['C',[0,1,0],+,['H',[0,1,0]],['H',[0,1,0]]]")
                        x[1][0][a2]="oxy"
                    if "o(" == a:
                        ylstelle=1
                        if 1 in secarg:
                            ylbindung=[0,secarg[1].count("i")+2,0]
                        else:
                            ylbindung=[0,1,0]
                        substituenten=dazu(["@0"+str(cyc2)+"C",["s1",1,0]],x[0]-1,substituenten)
                        lweg=True
                        andereseite="C"
                        if x[0]-1 in substituenten:
                            for i2 in substituenten[x[0]-1]:
                                if i2 in csubs.keys():
                                    andereseite=csubs[i2][0]
                        oklatur.append([i,andereseite,str(cyc2)])
                        cyc2+=1
                    if "azo" == a:
                        ylstelle=i
                        ylbindung=[0,1,0]
                        bruecke=bruecken(bruecke,"['N',[0,1,0],['N',[0,2,0],+]]")
                    if "amid" == a:
                        a2=["H",[0,1,0]]
                        a3=["H",[0,1,0]]
                        if amidaminolist!=[]:
                            a2=amidaminolist.pop(0)
                            if amidaminolist!=[]:
                                a3=amidaminolist.pop(0)
                            if not i in substituenten:
                                substituenten.__init__({i:[]})
                        elif i in substituenten:
                            a2=substituenten[i][-1]
                            del substituenten[i][-1]
                            if substituenten[i]!=[]:
                                a3=substituenten[i][-1]
                                del substituenten[i][-1]
                        elif coeftestwuerdig!=[]:
                             a2=analysezusyntax(x[coeftestwuerdig[0]])[1]
                             coeftestwuerdig=coeftestwuerdig[1:]
                        if (i==1 or i==x[0]) and not "cyclo" in x[2]:
                            substituenten=dazu(["O",[0,2,0]],i,substituenten)
                            substituenten[i].append(["N",[0,1,0],a3,a2])
                        else:
                            substituenten[i].append(["C",[0,1,0],["O",[0,2,0]],["N",[0,1,0],a3,a2]])
                    if "oyl" == a:
                        ylstelle=i
                        ylbindung=[0,1,0]
                        if (i==1 or i==x[0]) and not "cyclo" in x[2]:
                            substituenten=dazu(["O",[0,2,0]],i,substituenten)
                        else:
                            bruecke=bruecken(bruecke,"['C',[0,1,0],['O',[0,2,0]],+]")
                    if a in ("saeure","carbonsaeure"):
                        if (i==1 or i==x[0]) and not "cyclo" in x[2] and a=="saeure":
                            substituenten=dazu(["O",[0,1,0],["H",[0,1,0]]],i,substituenten)
                            substituenten[i].append(["O",[0,2,0]])
                        else:
                            substituenten=dazu(["C",[0,1,0],["O",[0,2,0]],["O",[0,1,0],["H",[0,1,0]]]],i,substituenten)
                    if "persaeure" == a:
                        if (i==1 or i==x[0]) and not "cyclo" in x[2]:
                            substituenten=dazu(["O",[0,2,0]],i,substituenten)
                            substituenten[i].append(["O",[0,1,0],["O",[0,1,0],["H",[0,1,0]]]])
                        else:
                            substituenten=dazu(["C",[0,1,0],["O",[0,2,0]],["O",[0,1,0],["O",[0,1,0],["H",[0,1,0]]]]],i,substituenten)
                    if "saeureanhydrid" == a:
                        subs=0
                        for sny in x[3:]:
                            if "saeure" in str(sny):
                                subs=sny
                                x.remove(sny)
                                sny=sny[0]
                                for i in sny[1]:
                                    if "saeure" in sny[1][i]:
                                        sny[1][i].remove("saeure")
                                        if "cyclo" in sny[2]:
                                            sny[1][i].append("eigentlichyl")
                                        sny[1][i].append("oyl")
                                        break
                                x2=analysezusyntax(sny)[1]
                                break
                        if subs==0:
                            x2=oldcopy.copy(x)
                            x2[1][i].remove("saeureanhydrid")
                            x2[1][i].append("oyl")
                            if "cyclo" in x2[2]:
                                x2[1][i].append("eigentlichyl")
                            x2=analysezusyntax([x2,i])[1]
                            x[1][i].remove("oyl")
                        x2=["O",[0,1,0],x2]
                        if i in (1,x[0]) or "cyclo" in x[2]:
                            substituenten=dazu(x2,i,substituenten)
                            substituenten[i].append(["O",[0,2,0]])
                        else:
                            substituenten=dazu(["C",[0,1,0],["O",[0,2,0]],["O",[0,1,0],x2]],i,substituenten)
                    if a in ("on","aldehyd","al"):
                        if a in ("aldehyd","al") and ("cyclo" in x[2] or i not in (1,x[0])):
                            substituenten=dazu(["C",[0,1,0],["O",[0,2,0]],["H",[0,1,0]]],i,substituenten)
                        else:
                            substituenten=dazu(["O",[0,2,0]],i,substituenten)
                    if "nitril"==a:
                        if "cyclo" in x[2] or i not in (1,x[0]):
                            substituenten=dazu(["C",[0,1,0],["N",[0,3,0]]],i,substituenten)
                        else:
                            substituenten=dazu(["N",[0,3,0]],i,substituenten)
                    if "thiol"==a:
                        substituenten=dazu(["S",[0,1,0],["H",[0,1,0]]],i,substituenten)
                    if "thial"==a:
                        substituenten=dazu(["S",[0,2,0]],i,substituenten)
                    if "eigentlichyl" in a:
                        ylstelle3=i
                    if "ol"==a:
                        if "aldehyd" in x[1][i]:
                            continue
                        substituenten=dazu(["O",[0,1,0],["H",[0,1,0]]],i,substituenten)
                    if a in ("yl","yliden","ylidin","ylen","ylin"):
                        if ylstelle!=0:
                            if i>x[0]:
                                i=x[0]
                            ylstelle2=i
                        else:
                            ylstelle=i
                            if "yl" == a:
                                ylbindung=[0,1,0]
                            elif a in ("yliden","ylen"):
                                ylbindung=[0,2,0]
                            elif a in ("ylidin","ylin"):
                                ylbindung=[0,3,0]
                    if "carbonyl"==a:
                        if bruecke:
                            bruecke=bruecken(bruecke,"['C',[0,1,0],['O',[0,2,0]],*]".replace("*",bruecke))
                        else:
                            bruecke=bruecken(bruecke,"['C',[0,1,0],['O',[0,2,0]],+]")
            if Endungslokantenfehler:
                fehlerapp.Endungsfehler(Endungslokantenfehler)
            last=0
            for i in coeftestwuerdig:
                if type(x[i][0][0])==type(1) and not "yl" in str(x[i][0][1]) and not "oyl" in str(x[i][0][1])and not "oxy" in str(x[i][0][1]) and not "azo" in str(x[i][0][1])and not "o(" in str(x[i][0][1])and not "azano" in str(x[i][0][1])and not "azeno" in str(x[i][0][1]):
                    continue
                if "o-" in x[i][0][2]:
                    ctwlist=[1,2,6]
                elif "m-" in x[i][0][2]:
                    ctwlist=[1,3,5]
                elif "p-" in x[i][0][2]:
                    ctwlist=[1,4]
                else:
                    ctwlist=range(1,x[0]+1)
                if last==0:
                    last=ctwlist[0]
                for i4 in ctwlist[ctwlist.index(last):]+ctwlist[:ctwlist.index(last)+1]:
                    summe=2
                    if i4==1:
                        summe=summe+1
                    if i4==x[0]:
                        summe=summe+1
                    if i4 in substituenten:
                        for i5 in range(len(substituenten[i4])):
                            summe=summe-substituenten[i4][i5][1][1]
                    if i4 in secarg:
                        summe=summe-secarg[i4][1]+1
                    if i4-1 in secarg:
                        summe=summe-secarg[i4-1][1]+1
                    if ylstelle==i4:
                        summe=summe-ylbindung[1]
                    if "cyclo" in x[2] and i4 in (1,x[0]):
                        summe=summe-1
                    if summe>0:
                        if check and i==coeftestwuerdig[-1]:
                            return i4
                        x[i][1]=i4
                        last=i4
                        break
                else:
                    x[i][1]=x[0]+1
                if check:
                    return 1
                a=analysezusyntax(x[i])
                if type(a[0])==type("a"):
                    return a
                if "+" in str(a[1]):
                    multiplikation+=[[a[0],1,a[1]]]
                    continue
                if type(a[1][1])==type(1):
                    triarg.__init__({a[0]:a[1]})
                else:
                    if a[2]!=0:
                        per=a[1]
                    else:
                        if a[0] in substituenten:
                            substituenten[a[0]].append(a[1])
                        else:
                            substituenten.__init__({a[0]:[a[1]]})
                if a[3]!=0:
                    chzentren.append([a[0],a[3]])
            s=[]
            for i in range(len(multiplikation)):
                exec("substituenten"+str(i+2)+"={}")
            for i in substituenten.keys():
                if type(i)==type("1'"):
                    ics=i.count("'")
                    exec("substituenten"+str(ics+1)+str([int(i[:i.index("'")])])+"=substituenten.pop(i)")
            for i in range(len(multiplikation)):
                alkan=lineare_aliphaten(x[0],secarg,eval("substituenten"+str(i+2)),triarg,per,zentral,cyclo,stelle=2)
                alkan[1]=[0,1,0]
                if multiplikation[i][2]==0:
                    bruecke2="'+'"
                else:
                    bruecke2=str(multiplikation[i][2])
                substituenten=dazu(eval(bruecke2.replace("'+'",str(alkan))),multiplikation[i][0],substituenten)
            if nochdran:
                if nochdran[1]:
                    #Umleitung in Verlaengerung bei Lactamen, Lactonen etc
                    substituentenumleitung={}
                    secargumleitung={}
                    triargumleitung={}
                    for i in substituenten:
                        if i>=nochdran[0]:
                            substituentenumleitung[i-nochdran[0]]=substituenten[i]
                            substituenten[i]=[]
                    for i in secarg:
                        if i>=nochdran[0]:
                            secargumleitung[i-nochdran[0]]=secarg[i]
                            secarg[i]=[0,1,0]
                    for i in triarg:
                        if i>=nochdran[0]:
                            triargumleitung[i-nochdran[0]]=triarg[i]
                            triarg[i]=zentral
                    cyclo2=0
                    if 0 in nochdran[3]:
                        cyclo2=1
                        if nochdran[1] in substituenten:
                            substituentenumleitung[nochdran[1]].insert(["@1C",[0,1,0]])
                        else:
                            substituentenumleitung[nochdran[1]]=[["@1C",[0,1,0]]]
                    substituent=lineare_aliphaten(nochdran[1],secargumleitung,substituentenumleitung,triargumleitung,per,zentral,cyclo2,ylstelle3=str(nochdran[0]))
                    if 0 in nochdran[3]:
                        substituent=substituent[2]
                    if per in substituent:
                        substituent[1],substituent[substituent.index(per)]=substituent[substituent.index(per)],substituent[1]
                    substituent[1]=[0,1,0]
                    substituenten=dazu(substituent,nochdran[0],substituenten)
                for i in nochdran[2]:
                    substituenten=dazu(nochdran[2][i].pop(0),i,substituenten)
                    substituenten[i]+=nochdran[2][i]
                for i in nochdran[3]:
                    triarg[i]=nochdran[3][i]
            if ylstelle!=0:
                if "poly" in x[2]:
                    substituenten=dazu(["polyhier",[0,1,0]],ylstelle2,substituenten)
                if ylstelle in triarg:
                    triarg[ylstelle][0]+="*"
                else:
                    triarg.__init__({ylstelle:[zentral[0]+"*",zentral[1]]})
                if oklatur:
                    if x[0]-1 in triarg:
                        oklatur[-1][1]=triarg[x[0]-1][0]
                for i in x[2]:
                    if i[0]=="[":
                        i=eval(i)
                        chzentren.append([i[1],{"(s)":"links","(r)":"rechts"}[i[0]]])
                for i in chzentren:
                    if i[0] in triarg.keys():
                        triarg[i[0]][0]+="~"+i[1]
                    else:
                        triarg[i[0]]=[zentral[0]+"~"+i[1],zentral[1]]
                alkan=Chiralitaetszentrenordner(lineare_aliphaten(x[0],secarg,substituenten,triarg,per,zentral,cyclo,stelle=2,lweg=lweg,ylstelle3=ylstelle3))
                i=1
                if ylbindung==[0,3,0]:
                    alkan=alkan[:3]
                    alkan[1]=[0,3,0]
                else:
                    if ylbindung==[0,2,0]:
                        while True:
                            if alkan[i]==per:
                                alkan[i]=alkan[1]
                                del alkan[1]
                                break
                            if i==len(alkan):
                                break
                            i+=1
                    while True:
                        if alkan[i]==per:
                            alkan[i]=alkan[1]
                            break
                        if i==len(alkan)-1:
                            break
                        i+=1
                    alkan[1]=ylbindung
                if "bi" in x[2]:
                    return [alkan[0],alkan]+alkan[2:]
                umtausch=[]
                if "thio" in x[2]:
                    umtausch.append("S")
                if "seleno" in x[2]:
                    umtausch.append("Se")
                if "telluro" in x[2]:
                    umtausch.append("Te")
                if "pollonio" in x[2]:
                    umtausch.append("Po")
                alkan=str(alkan)
                for um in umtausch:
                    alkan=str(alkan)
                    if "O" in alkan:
                        o=alkan.index("O")
                        alkan=alkan[:o]+um+alkan[o+1:]
                alkan=eval(alkan)
                if bruecke!="":
                    alkan=eval(bruecke.replace("+",str(alkan)))
                if "poly" in x[2]:
                    alkan2=oldcopy.copy(alkan)
                    for i in range(mi-1):
                        alkan=eval(str(alkan).replace("['polyhier', [0, 1, 0]]",str(alkan2)))
                    alkan=eval(str(alkan).replace("['polyhier', [0, 1, 0]]",str(zweites_polymerende)))
                    alkan[1]=erstes_polymerende
                    return alkan
                return [stelle,alkan,per2,lr,oklatur]
            for i in range(len(x[2])):
                if x[2][i][:8]=="bicyclo[":
                    bicyclo=split(x[2][i][8:-1],".")
                    for i in range(len(bicyclo)):
                        bicyclo[i]=int(bicyclo[i])
                    x[0]=bicyclo[0]+2
                    zweiter_ring=[bicyclo[1]+2,{},{},{}]
                    for i in secarg:
                        if i>x[0]:
                            zweiter_ring[1].__init__({i-x[0]:secarg[i]})
                    for i in substituenten.keys():
                        if i>x[0]:
                            zweiter_ring[2].__init__({i-x[0]+1:substituenten[i]})
                    for i in triarg:
                        if i>=x[0]:
                            zweiter_ring[3].__init__({i-x[0]+1:triarg[i]})
                    zweiter_ring=lineare_aliphaten(zweiter_ring[0],zweiter_ring[1],zweiter_ring[2],zweiter_ring[3],per,zentral,2,stelle=2)
                    zweiter_ring=zweiter_ring[3]
                    zweiter_ring[1][2]=0
                    zweiter_ring[2][1][2]
                    if 1 in substituenten:
                        substituenten[1].append(zweiter_ring)
                    else:
                        substituenten.__init__({1:[zweiter_ring]})
                    cyclo=1
            for i in x[2]:
                if i[0]=="[" or i in ("(s)","(r)"):
                    if i[0]=="[":
                        i=eval(i)
                    else:
                        i=[i,1]
                    chzentren.append([i[1],{"(s)":"links","(r)":"rechts"}[i[0]]])
            for i in chzentren:
                if i[0] in triarg.keys():
                    triarg[i[0]][0]+="~"+i[1]
                else:
                    triarg[i[0]]=[zentral[0]+"~"+i[1],zentral[1]]
            alkan=lineare_aliphaten(x[0],secarg,substituenten,triarg,per,zentral,cyclo,lweg=lweg)
            for i in chzentren:
                alkan=str(alkan)
                for i1 in range(len(alkan)):
                    if alkan[i1]=="~":
                        if alkan[i1+1:].startswith("links"):
                            lr="links"
                        else:
                            lr="rechts"
                        alkan=alkan[:i1]+"*"+alkan[i1+1+len(lr):]
                        alkan=eval(alkan)
                        break
                alkan=Chiralitaetszentrenordner(alkan,lr)
            if bruecke!="":
                alkan=eval(bruecke.replace("+",str(alkan)))
            alkan=str(alkan)
            umtausch=[]
            if "thio" in x[2]:
                    umtausch.append("S")
            if "seleno" in x[2]:
                umtausch.append("Se")
            if "telluro" in x[2]:
                umtausch.append("Te")
            if "pollonio" in x[2]:
                umtausch.append("Po")
            alkan=str(alkan)
            for um in umtausch:
                alkan=str(alkan)
                if "O" in alkan:
                    o=alkan.index("O")
                    alkan=alkan[:o]+um+alkan[o+1:]
            while "~" in alkan:
                i1=alkan.index("~")
                if alkan[i1+1:].startswith("links"):
                    lr="links"
                else:
                    lr="rechts"
                alkan=alkan[:i1]+"*"+alkan[i1+1+len(lr):]
                alkan=eval(alkan)
                alkan=str(Chiralitaetszentrenordner(alkan,lr))
            return eval(alkan)
        else:
            zentral=info("suffix",x[0])
            anzahl1bindungen=zentral.count('"+"')
            anzahl2bindungen=zentral.count('"++"')
            anzahl3bindungen=zentral.count('"+++"')
            if "bi" in x[2]:
                z2=zentral
                a=z2.index('"+"')
                if eval(z2)[1]!="+":
                    z2=z2[:a]+str(eval(z2)[1])+z2[a+3:]
                z2=eval(z2)
                if anzahl1bindungen!=0:
                    exec("z2[1]=[0,1,0]")
                elif anzahl2bindungen!=0:
                    exec("z2[1]=[0,2,0]")
                elif anzahl2bindungen!=0:
                    exec("z2[1]=[0,3,0]")
                z2=str(z2)
                z2=z2.replace(', "+"',"")
                substituenten={1:[eval(z2)]}
            for i1 in substituenten:
                for i in substituenten[i1]:
                    i2={1:'"+"',2:'"++"',3:'"+++"'}[i[1][1]]
                    a=zentral.index(i2)
                    zentral=zentral[:a]+str(i)+zentral[a+len(i2):]
            return eval(zentral)
def bruecken(x,a):
    if x:
        return a.replace("+",x)
    else:
        return a
def hoechstesaussphere(x,_sphere):
    angebot=[]
    if _sphere==0:
        if "@" in x[0]:
            return [0,0]
        return [_ordnungszahl(x[0]),x[1][1]]
    if len(x)==2:
        return [0,0]
    for i in x[2:]:
        angebot.append(hoechstesaussphere(i,_sphere-1))
    _max=max(angebot)
    _max.append(angebot.count(_max))
    return _max
def _ordnungszahl(x):
    return eval("symbol"+str(ohnezahlen(x))).ordnungszahl
def dazu(x,stelle,var):
    if stelle in var:
        var[stelle].append(x)
    else:
        var[stelle]=[x]
    return var
def substituiere(x,y):
    bindung=y[1][1]
    h1=0
    for i in x[1:]:
        if i[0]=="H":
            h1+=1
    if h1>=bindung:
        h2=0
        for i in range(1,len(x)):
            if x[i][0]=="H":
                h2+=1
                if h2==bindung:
                    x[i]=y
                    for i in range(x.count("*")):
                        x.remove("*")
                    return x
                x[i]="*"
                i-=1
    for i in x[2:]:
        if len(i)>2:
            temp=substituiere(i,y)
            if temp!=False:
                x[x.index(i)]=temp
                return x
    return False
def lineare_aliphaten(x,y,sonderwuensche={},Csub={},per=["H",[0,1,0]],zentral=["C",4],cyclo=0,stelle=1,lweg=False,ylstelle3=False):
    global cyc,bt,annelierungsbindung,fehlerapp
    wertigkeit=zentral[1]
    zentral=zentral[0]
    stelle+=1
    if x in (1,2) and cyclo:
        fehlerapp.Cyclofehlerzuklein(x)
        cyclo=False
        if x in sonderwuensche.keys():
            for i in sonderwuensche[x]:
                if "@" in i[0]:
                    sonderwuensche[x].remove(i)
                    break
    if per[1][1]!=1 and 1 not in y:
        alkan=["H",[0,1,pi]]
    elif cyclo==0:
        if x in sonderwuensche:
            h=0
            for i in sonderwuensche[x]:
                if len(i[1])==4 and i[1][3] in ("1","0"):
                        continue
                if i[1][1]==1:
                    alkan=i
                    sonderwuensche[x].remove(i)
                    if sonderwuensche[x]==[]:
                        del sonderwuensche[x]
                    if alkan[0]!="polyhier" and type(alkan[1][2])!=type("cis1"):
                        alkan[1][2]=pi
                    h=1
                    break
            if h==0:
                alkan=per[:1]+[[0,per[1][1],pi]]+per[2:]
        else:
            alkan=per[:1]+[[0,per[1][1],pi]]+per[2:]
    else:
        alkan=per
    stelle2=0
    if cyclo!=0:
        if lweg:
            s=alizyklen(x,y,sonderwuensche)
            y2={}
            for i in y:
                y2[i-2]=y[i]
            y=y2
        else:
            s=alizyklen(x,y,sonderwuensche)
        if 1 in Csub:
            cychilfe=ohnezahlen(Csub[1][0].replace("*",""))
        else:
            cychilfe=zentral
        if type(s)==type(1.3):
            s1=radians(109.48)
            s2=s
        elif len(s)==3:
            s1=s[0]
            s2=s[1]
        else:
            s1=s[0]
            s2=0
        if stelle==3:
            if s2==0:
                stelle2=2
            else:
                stelle2=1
            stelle=2
        annelierungsbindung=s1
        if x in sonderwuensche:
            sonderwuensche[x].insert(0,["@"+str(cyc)+cychilfe,[s1,1,s2,0]])
        else:
            sonderwuensche[x]=[["@"+str(cyc)+cychilfe,[s1,1,s2,0]]]
        if lweg and len(sonderwuensche[x-1])>1:
            for i in range(len(sonderwuensche[x-1])):
                if "@" in sonderwuensche[x-1][i][0]:
                    sonderwuensche[x-1][i],sonderwuensche[x-1][0]=sonderwuensche[x-1][0],sonderwuensche[x-1][i]
                    break
        sonderwuensche=eval(str(sonderwuensche).replace("'s1'",str(s1)))
        if x in Csub:
            cychilfe=ohnezahlen(Csub[x][0].replace("*",""))
        else:
            cychilfe=zentral
        if 1 in sonderwuensche:
            sonderwuensche[1].insert(0,["@"+str(cyc)+cychilfe,[s1,1,0,0]])
        else:
            sonderwuensche[1]=[["@"+str(cyc)+cychilfe,[s1,1,0,0]]]
        cyc+=1
        for i in y.keys():
            y[i][0]=s1
            y[i][2]=s2
    else:
        s1=0
        s2=pi
    i=0
    while i!=x:
        if i==0 and lweg:
            i+=1
        s2*=-1
        temp2=[s1,1,s2]
        if i==0:
            temp2=[s1,1,s2,0]
        if x-i in y:
            temp2=y[x-i]
        temp3=[s1,1,s2,0]
        if x-i-2 in y:
            temp3=y[x-i-2]
        if x-i==2:
            temp3=[s1,1,s2]
        if lweg and i==1:
            temp2=[0,1,0]
        if x-i-1 in y:
            if bt==10:
                temp=y[x-i-1]
            else:
                temp=y[x-i-1]+[0]
            temp[2]=s2
        else:
            if x-i in y and y[x-i][1]==2 and cyclo==0:
                temp=[s1,1,s2]
                if type(y[x-i][2])==type("cis"):
                    temp[2]=y[x-i][2]
            elif x-i-2 in y and y[x-i-2][1]==2 and cyclo==0:
                temp=[s1,1,s2]
                if type(y[x-i-2][2])==type("cis"):
                    temp[2]=y[x-i-2][2]
            else:
                temp=[s1,1,s2,0]
                if bt==10:
                    temp.pop()
        if cyclo:
            temp[3]=1
        if x-i==3:
            if stelle2==1:
                temp[2]=temp[2]+2*pi/3
            elif stelle2==2:
                temp[2]=temp[2]+pi
        if temp[1]>1 and temp[2]!=0:
            temp[2]=0
        atom=[zentral,wertigkeit]
        a=1
        if x-i in Csub:
            atom=Csub[x-i]
        if ylstelle3:
            if type(ylstelle3)==str:
                s3=x-i+eval(ylstelle3)
            else:
                s3=(x-i+ylstelle3-2)%x+1
        else:
            s3=x-i
        neue_methylgruppe=[atom[0]+str(s3),temp]
        zusatz=0
        if per[1][1]==2 and atom[1]+1-temp[1]-temp2[1]!=2:
             neue_methylgruppe.append(["H",[0,1,0]])
        for n in range((atom[1]+1-temp[1]-temp2[1]-zusatz)/(per[1][1])):
            neue_methylgruppe+=[per]
        if len(neue_methylgruppe)==2:
            neue_methylgruppe.append(alkan)
        elif len(neue_methylgruppe)<=stelle:
            neue_methylgruppe[-1]=alkan
        else:
            neue_methylgruppe[stelle]=alkan
        alkan=neue_methylgruppe
        if x-i==1:
            if 1 in sonderwuensche:
                sonderwuensche.__init__({-1:sonderwuensche[1][0]})
                sonderwuensche[1]=sonderwuensche[1][1:]
                for n in range(sonderwuensche[-1][1][1]-1):
                    for a in range(2,len(alkan)):
                        if alkan[a]==per:
                            del alkan[a]
                            break
                    else:
                        break
        while x-i in sonderwuensche:
            if sonderwuensche[x-i]==[]:
                break
            for a in range(2,len(alkan)):
                if cyclo==1 and type(sonderwuensche[x-i][0][1][2])==type("cistrans"):
                    if sonderwuensche[x-i][0][1][2][:3]=="cis":
                        a=(x-i+1)%2+3
                    else:
                        a=(x-i)%2+3
                    sonderwuensche[x-i][0][1][2]=0
                if alkan[a]==per:
                    alkan[a]=sonderwuensche[x-i][0]
                    if sonderwuensche[x-i][0][1][1]>1 and cyclo!=0:
                        if s1==0:
                            alkan[1][0]=radians(109.5)
                        else:
                            alkan[1][0]=s1
                    sonderwuensche[x-i]=sonderwuensche[x-i][1:]
                    break
            if type(alkan[a][0])!=type(1):
                for n in range(alkan[a][1][1]-1):
                    for a in range(2,len(alkan)):
                        if alkan[a]==per:
                            del alkan[a]
                            break
            if sonderwuensche[x-i]==[]:
                break
            if a==len(alkan)-1:
                alkan.append(sonderwuensche[x-i][0])
                sonderwuensche[x-i]=sonderwuensche[x-i][1:]
        for a in range(2,len(alkan)):
            if len(alkan[a][1])==4 and alkan[a][1][3] in ("1","0"):
                if alkan[a][1][3]=="1":
                    alkan[a][1]=alkan[a][1][:3]
                    if stelle==2:
                        alkan[3],alkan[a]=alkan[a],alkan[3]
                    elif len(alkan)>=5:
                        alkan[4],alkan[a]=alkan[a],alkan[4]
                else:
                    alkan[a][1]=alkan[a][1][:3]
                    if stelle==2 and len(alkan)>=5:
                        alkan[4],alkan[a]=alkan[a],alkan[4]
                    elif len(alkan)>=5:
                        alkan[2],alkan[a]=alkan[a],alkan[2]
                break
        i+=1
    specialwinkel=alkan[1][0]
    if x-1 not in y and per[1][1]!=1:
        if alkan[1][0]!=0:
            alkan[1]=["H",[alkan[1][0],1,0]]
        else:
            ["H",[0,1,0]]
    else:
        alkan[1]=per
    if x==2:
        if alkan[1][1][1]==1 and alkan[2][1][1]==1:
            alkan[2][1][2]=pi/3
    if -1 in sonderwuensche:
        sonderwuensche[-1][1][0]=specialwinkel
        alkan[1]=sonderwuensche[-1]
        if sonderwuensche[-1][1][1]>1 and cyclo!=0:
            if s1==0:
                alkan[stelle][1][0]=radians(109.5)
            else:
                alkan[stelle][1][0]=s1
    if stelle2==1:
        alkan=alkan[:2]+[alkan[3],alkan[2]]+alkan[4:]
    return alkan
def ohnezahlen(x):
    if x[0]=="@":
        if "~" in x:
            return x[:x.index("~")]
        return x
    if "~" in x:
        x=x[:x.index("~")]
    while x[-1] in digits:
        x=x[:-1]
        if x=="":
            break
    return x
def mitzahlen(x):
    if x[0]=="@":
        return x
    while x[0] in letters:
        x=x[1:]
        if x=="":
            break
    return x
def Chiralitaetszentrenordner(x,lr=0,stern="*"):
    x=str(x)
    if not "*" in x:
        return eval(x)
    i=x.index("*")
    ind=x.index(",")
    #das Zeichen "~?" steht für das eigentliche Zentralatom
    #"~" ist wichtig, damit ohnezahlen(x) das fragezeichen nicht beachtet
    x=x
    xauf=x[1:i].count("[")
    if xauf==0:
        x=x.replace("*","")
        x=eval(x)
        if lr!=0:
            return CIPprioritaetenordner(x,lr)
        return x
    x=x[:ind-1]+"~?"+x[ind-1:]
    xzu=x[1:i].count("]")
    l=0
    k=[]
    for n in range(xauf):
        k.append(0)
    for n in range(len(x[:i])):
        if x[n]=="[":
            l+=1
        elif x[n]=="]":
            l-=1
            for o in range(l,len(k)):
                k[o]=0
        elif x[n]==",":
            k[l-1]+=1
    while k[-1]==0:
        k=k[:-1]
    x=eval(x)
    y=eval("x"+str(k).replace(",","]["))
    b=y[1]
    exec("x"+str(k).replace(",","][")+"='#'")
    z="'#'"
    for i in range(len(k)-1,0,-1):
        z2=eval("x"+str(k[:i]).replace(",","]["))
        exec("x"+str(k[:i]).replace(",","][")+"='#'")
        b,z2[1]=z2[1],b
        z=z.replace("'#'",str(z2))
    x[0]+="*"
    h1=x.index('#')
    x=eval(str(x).replace("'#'",str(b)))
    x[1],x[h1]=b,x[1]
    if len(x)==5 and h1!=1:
        h=[2,3,4]
        h.remove(h1)
        x[h[0]],x[h[1]]=x[h[1]],x[h[0]]
    z=z.replace("'#'",str(x))
    y[1]=eval(z.replace("*",""))
    if lr!=0:
        y=CIPprioritaetenordner(y,lr)
        y=eval(str(y).replace("~?","*"))
        #Der Stern wird gelöscht, das ursprüngliche Zentralatom wird zurückgeordnet
        y=Chiralitaetszentrenordner(y)
        #Bei der Ordnung tritt ein Fehler auf,
        #das erste und zweite element muss bei Alkanen vertauscht werden
        if len(y[1][1])==4:
            y[1],y[2]=y[2],y[1]
    y=eval(str(y).replace("*","").replace("~?",""))
    return y
def hoechste_ordnungszahl_finder(syntax):
    l=[]
    for i in syntax[1:]:
        for n in range(len(i[1])):
            l.append(atom_color(i[0])[2])
    return [max(l),l.count(max(l))]
def CIPprioritaetenordner(syntax,lr):
    reihenfolge=[]
    syntax2=cyclotraeumer(syntax)
    for i in range(1,len(syntax)):
        if "@" in syntax2[i][0]:
            acs=syntax2[i][0][1:]
            while acs[0] in digits:
                acs=acs[1:]
        else:
            acs=ohnezahlen(syntax2[i][0])
        reihenfolge.append([[_ordnungszahl(acs),syntax2[i][1]]])
    for i in reihenfolge:
        i[0][1]=i[0][1][1]
    for i in range(len(reihenfolge)):
        while reihenfolge.count(reihenfolge[i])!=1:
            bearbeitungsbedarf=[i]
            for n in range(len(reihenfolge)):
                if n==i:
                    continue
                if reihenfolge[n]==reihenfolge[i]:
                    bearbeitungsbedarf.append(n)
            geradedazu=[]
            for n in bearbeitungsbedarf:
                geradedazu.append(hoechstesaussphere(syntax2[n+1],len(reihenfolge[n])))
                reihenfolge[n]=geradedazu[-1]
            if geradedazu.count([0,0])==len(geradedazu):
                for i2 in bearbeitungsbedarf:
                    reihenfolge[n]=[i2,1,1]
                break
    richtige_reihenfolge=[]
    reihenfolge2=oldcopy.copy(reihenfolge)
    reihenfolge2.sort()
    for i in reihenfolge:
        richtige_reihenfolge.append(reihenfolge2.index(i))
    for prioritaet in range(3):
        p_index=richtige_reihenfolge.index(prioritaet)
        if prioritaet!=p_index:
            richtige_reihenfolge[p_index],richtige_reihenfolge[prioritaet]=richtige_reihenfolge[prioritaet],richtige_reihenfolge[p_index]
            if lr=="links":
                lr="rechts"
            else:
                lr="links"
    nichtkonst=[3,4]
    for i in (0,1):
        for i2 in range(len(syntax2[2:])):
            if len(syntax[i2+2][1])!=4:
                if not i2+2 in nichtkonst:
                    nichtkonst[i]=i2+2
        else:
            for i2 in range(len(syntax2[2:])):
                if not (len(syntax2[i2+2][1])==4 and syntax2[i2+2][1][3]==1):
                    if not i2+2 in nichtkonst:
                        nichtkonst[i]=i2+2
                        break
    if lr=="links":
        syntax[nichtkonst[0]],syntax[nichtkonst[1]]=syntax[nichtkonst[1]],syntax[nichtkonst[0]]
    return syntax
def cyclotraeumer(syntaxb):
    markt={}
    syntaxb[0]=syntaxb[0].replace("*","")
    x2=str(syntaxb)
    x=str(syntaxb)
    if not "@" in x:
        return syntaxb
    for i in range(len(x)):
        if x[i]=="@":
            zahl=""
            i1=1
            while x[i+i1] in digits:
                zahl+=x[i+i1]
                i1+=1
            markt=dazu(str(Chiralitaetszentrenordner(eval(x[:i+1]+"*"+x[i+1:]),0)[1]),eval(zahl),markt)
    i=0
    while i<len(x2):
        if x2[i]=="@":
            zahl=""
            i1=1
            while x2[i+i1] in digits:
                zahl+=x2[i+i1]
                i1+=1
            ind=ntesvorkommen(x2[i:],"]",2)+1
            x2=x2[:i-2]+markt[eval(zahl)][-1]+x2[i+ind:]
            i+=len(markt[eval(zahl)].pop())-4
        i+=1
    return eval(x2)
def ntesvorkommen(x,y,n):
    if n==0:
        return -1
    ind=x.index(y)+1
    return ind+ntesvorkommen(x[ind:],y,n-1)
def alizyklen(x,y,sub):
    global fehlerapp
    if x==4 and y=={}:
        return 1.5,0.43633231299858238,"envelope"
    if x==5 and y=={}:
        return 1.86,0.2,"envelope"
    lengthB=10
    if x in (1,2):
        return 0
    if x==3:
        return pi/3,"planar"
    y3=[]
    for i in range(1,x+1):
        if i not in y:
            y3.append(1)
        else:
            y3.append(y[i][1])
    contraplanar=[]
    y3.append(y3[0])
    for i in range(x):
        if y3[i+1]==1 and y3[i]==1 and y3[i-1]==1:
            contraplanar.append(i+1)
    if contraplanar==[] or x==4 or (len(contraplanar)<3 and x==5):
        return pi-pi*2/x,"planar"
    gamma=-radians(54.75)-arcsin(tan((2.*pi/x)/-2.)*cos(radians(19.5))*sin(pi/3.)/cos(radians(54.75)))
    gamma=rotate(rotate(rotate(vector(0,1,0),gamma,vector(0,0,1)),1.*pi/x,vector(0,1,0)),radians(-19.5),vector(1,0,0))
    gamma[2]=0
    gamma=pi/3.+2.*diff_angle(gamma,vector(0,1,0))
    if x>5 and len(contraplanar)!=x:
        fehlerapp.Cyclofehler(x)
    return gamma
def coefs(x):
    global greek1,snl
    weg=""
    s1c1=[]
    greek=False
    while True:
        xcoef=""
        while x[0] in digits:
            xcoef+=x[0]
            x=x[1:]
        else:
            if xcoef=="":
                if (len(x)>2 and x[:3] in snl) or (len(x)>3 and x[:4] in snl):
                    s1c1.append(x[:x.index("*")].capitalize())
                    x=x[x.index("*")+2:]
                    continue
                h=0
                for i in greek2:
                    if x.startswith(lower(i)):
                        greek=True
                        s1c1.append(greek2.index(i)+2)
                        x=x[len(i):]
                        h=1
                        break
                if h==0 and s1c1==[]:
                    return ["",x,0,0]
            elif x[0]=="'":
                s=""
                while x[0]=="'":
                    s+="'"
                    x=x[1:]
                s1c1+=[xcoef+s]
            else:
                s1c1+=[int(xcoef)]
        if x[0]==",":
            x=x[1:]
            continue
        break
    greeks1c1=ncalkan(len(s1c1))
    if len(s1c1)==2:
        greeks1c1="di"
    if len(s1c1)==3:
        greeks1c1="tri"
    if len(s1c1)==1:
        greeks1c1="mono"
    if len(s1c1)==12:
        greeks1c1="dodeca"
    if x[0]=="-":
        x=x[1:]
    greeks1c12=False
    if len(s1c1)<9 and len(s1c1)>1:
        greeks1c12=["bis","tris","tetrakis","pentakis","hexakis","heptakis","oktakis","nonakis"][len(s1c1)-2]
    if greeks1c12 and x.startswith(greeks1c12):
        x=x[len(greeks1c12):]
        weg=greeks1c12
    elif x.startswith(greeks1c1):
        x=x[len(greeks1c1):]
        weg=greeks1c1
    elif len(s1c1)==2 and x.startswith("bis"):
        x=x[3:]
        weg=greeks1c12
    if x[0]=="-":
        x=x[1:]
    return [s1c1,x,weg,greek]
def aloescher(xi):
    if xi!="":
        if xi[0]=="a" and not xi.startswith("al") and not xi.startswith("amid") and not xi.startswith("an"):
            return xi[1:]
    return xi
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
def zwi(x):
    #ergaenzt am 1.11.08, soll die den Koeffizieten folgenden gr. Zahlw?rter l?schen
    #gez. Stefan:
    not_neccessary = ["di","tri","tetra","penta","hexa","hepta","octa","nona"]
    for i in range(0,8):
        if x.startswith(not_neccessary[i]):
            x = x[len(not_neccessary[i]):]

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
def sfrw(x,gangart=False):
    rl={"i":1,"v":5,"x":10,"l":50,"c":100,"m":1000}
    if gangart:
        if not x.startswith("("):
            return False
        x=x[1:]
        while x[0]!=")":
            if x=="":
                return False
            if x[0] not in rl.keys():
                return False
            x=x[1:]
        return True
    if x[0]=="(":
        x=x[1:]
    x+="#"
    zahl=[rl[x[0]]]
    x=x[1:]
    gesamt=0
    while x[0] not in ("#",")"):
        zahl.append(rl[x[0]])
        if zahl[0]<zahl[1]:
            gesamt-=zahl[0]
        else:
            gesamt+=zahl[0]
        zahl=[zahl[1]]
        x=x[1:]
    gesamt+=zahl[0]
    return gesamt
def praes(x):
    global csubs
    h=""
    p=praefix.keys()
    p.sort()
    p.reverse()
    for a in p:
        if x.startswith(a):
            h=a
            break
    for a in csubs.keys():
        if x.startswith(a):
            if len(a)>len(h):
                return (a,x[len(a):])
            else:
                return (h,x[len(h):])
    if h!="":
        return (h,x[len(h):])
    return ("",x)
def hantzsch_widmann(x):
    global csubs
    priorlist=["oxa","thia","selena","tellura","aza","phospha","arsa","stiba","bisma","sila","germa","stanna","plumba","bora","mercura"]
    csubs2=[]
    h=1
    anz=0
    x2=oldcopy.copy(x)
    aloesch=0
    while h==1:
        h=0
        if anz==0:
            temp=sfgw(x)
            if temp[0]!="":
                if temp[0] in ("metha","etha","propa","buta","undeca","enneadeca","icosa","henicosa"):
                    break
                else:
                    anz=ncalkan(temp[0])
                    x=temp[1]
            else:
                anz=1
        for i in csubs.keys():
            if x.startswith(i[:-1]):
                if csubs2!=[] and priorlist.index(i)<priorlist.index(csubs2[-1]):
                    break
                x=x[len(i[:-1]):]
                for n in range(anz):
                    csubs2.append(i)
                anz=0
                h=1
                break
        if h==0 and x!="" and x[0]=="a":
            if anz==1:
                anz=0
            h=1
            x=x[1:]
            aloesch=1
            continue
        elif h==1:
            aloesch=0
    if aloesch==1:
        x="a"+x
    if csubs2==[]:
        return [],x
    if anz not in(1,0):
        return [],x2
    ges=["epan","ocan","onan","ecan"]
    mnk=["epin","ocin","onin","ecin"]
    if    csubs[csubs2[-1]][0] in ["B","F","Cl","Br","I","P","As","Sb"]:
        mnk=["inin"]+mnk
        ges=["inan"]+ges
    elif  csubs[csubs2[-1]][0] in ["N","Si","Ge","Sn","Pb"]:
        mnk=["in"]+mnk
        ges=["inan"]+ges
    else:
        mnk=["in"]+mnk
        ges=["an"]+ges
    mnk=["et","ol"]+mnk
    if "aza" in csubs2:
        mnk=["irin"]+mnk
        ges=["iridin","etidin","olidin"]+ges
    else:
        mnk=["iren"]+mnk
        ges=["iran","etan","olan"]+ges
    for i in range(len(ges)):
        if x.startswith(ges[i]):
            return i+3,csubs2,x[len(ges[i]):],"ges"
    for i in range(len(mnk)):
        if x.startswith(mnk[i]):
            return i+3,csubs2,x[len(mnk[i]):],"mnk"
    return [],x2
def suffixe(x):
    for a in suffix.keys():
        if x.startswith(a):
            return(a,x[len(a):])
    for a in namen:
        if x.startswith(lower(a)):
            if x.startswith("seleno") or x.startswith("telluro") or x.startswith("polonio"):
                continue
            if sfrw(x[len(a):],True):
                a+=x[len(a):x.index(")")+1]
            return lower(a),x[len(a):]
    return "",x

def sonderz(x,k=False):
    global zuckerpraefixe
    sonderzeichen=["(z)","(e)","(s)","(r)","cyclo","per","bicyclo(","spiro(","bi","o-","m-","p-","thio","seleno","telluro","pollonio","poly","l*-","d*-","lambda(","delta("]
    if k:
        sonderzeichen[:4]=["z","e","s","r"]
    for a in sonderzeichen:
        if x.startswith(a):
            if a in ("bicyclo(","spiro(","delta"):
                a=a+x[len(a):x.index(")")+1]
            if a in ("delta(","lambda("):
                a=a+x[len(a):x.index(")")+1]
                return({"*":a},x[len(a):])
            return a,x[len(a):]
    if x.startswith("("):
        s={}
        y=x[1:]
        while y[0]!=")":
            c=coefs(y)
            if c[0]=="":
                return "",x
            y=c[1]
            temp=sonderz(y,True)
            if temp[0]=="":
                return "",x
            y=temp[1]
            if temp[0] in ("z","e","s","r"):
                temp=["("+temp[0]+")"]
            for i in c[0]:
                s=dazu(temp[0],i,s)
            while y[0] in (" ",",","-"):
                y=y[1:]
        return (s,y[1:])
    if x=="":
        return ("",x)
    if x[0] in ["-"," ",","]:
        x=x[1:]
    for i in zuckerpraefixe.keys():
        if x.startswith(i):
            x=x[len(i):]
            return [i,x,"zucker"]
            break
    return ("",x)
def generatoren():
    from string import lower
    from PSE import name
    from atome import atomlist
    import csv
    list={}
    reader = csv.reader(open("praefixe.csv", "rb"), delimiter=",")
    for row in reader:
        name2 = row[0]
        syntax = row[1]
        list.__init__({name2:syntax})
    f = file("praefixe.py","w")
    f.write(str("praefix=") + str(list))
    f.close()
    list={}
    reader = csv.reader(open("suffixe.csv", "rb"), delimiter=",")
    for row in reader:
        name = row[0]
        syntax = row[1]
        list.__init__({name:syntax})
    f = file("suffixe.py","w")
    f.write(str("suffix=") + str(list))
    f.close()
def beschreibung(x):
    global cis,trans
    cis=2
    trans=2
    return analysezusyntax(analyse(x))
def nuranalyse(x):
    print analyse(x)
def nurbeschreibung(x):
    print beschreibung(x)
def nurzeichnen(x):
    global scene
    scene=display()
    scene.select()
    scene.exit=False
    a=analysezusyntax(analyse(x))
    syntuxzuatomzeichnen(scene,a,1,1,1,10,1,1)
nuranalyse("Methylsulfonsaeure")
VP=False
def colorcompare(a):
    a2=[]
    for i in range(len(a)):
        round(a[i],3)
        a2.append(eval(str(a[i])[:5]))
    return a2
def dazu3(x):
    if x==1:
        return ""
    else:
        return str(x)
def mol_open():
	name3 = fileopenbox(msg=None, title="Bitte Molekuel waehlen...", default=None)
	return name3
def zuruck():
    atomlist={'Ru': [44, (0.5, 0.5, 0.5), 101.0, 4.2000000000000002, 1.0, 0, 2.2000000000000002],
'Re': [75, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 168.19999999999999, 5.2999999999999998, 1.0, 0, 1.8999999999999999],
'Ra': [88, (0.5, 0.0, 0.0), 226.0, 7.166666666666667, 2.0],
'Rb': [37, (0.69999999999999996, 0.0, 0.59999999999999998), 85.0, 7.0333333333333332, 1.0, 1, 0.80000000000000004],
'Rh': [45, (0.69999999999999996, 0.40000000000000002, 0.40000000000000002), 102.0, 4.5, 1.0, 0, 2.2999999999999998],
'Be': [4, (1.0, 1.0, 0.0), 9.0, 3.0, 1.0, 2, 1.6000000000000001],
'Ba': [56, (0.0, 0.80000000000000004, 0.59999999999999998), 137.0, 6.5999999999999996, 2.0, 2, 0.90000000000000002],
'Br': [35, (0.69999999999999996, 0.40000000000000002, 0.10000000000000001), 80.0, 3.7999999999999998, 7.0, 7, 3.0],
'H': [1, [1.0, 1.0, 1.0],1.0, 1.2333333333333334, 1.0, 1, 2.2000000000000002],
'P': [15, [1.0, 0.50196078431372548, 0.0],31.0, 3.5333333333333332, 5.0, 5, 2.2000000000000002],
'Os': [76, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 190.19999999999999, 4.2666666666666666, 1.0, 0, 2.2000000000000002],
'Ge': [32, (0.69999999999999996, 0.5, 0.29999999999999999), 72.599999999999994, 4.0666666666666664, 4.0, 4, 2.0],
'Gd': [64, (0.90000000000000002, 0.90000000000000002, 0.90000000000000002), 157.0, 5.9666666666666668, 1.0, 0, 1.2],
'Ga': [31, (0.59999999999999998, 0.59999999999999998, 0.5), 69.700000000000003, 4.2000000000000002, 3.0, 3, 1.8],
'Pr': [59, (0.80000000000000004, 1.0, 0.0), 140.90000000000001, 6.0666666666666664, 1.0, 0, 1.1000000000000001],
'Pt': [78, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 195.0, 4.5999999999999996, 1.0, 0, 2.2999999999999998],
'C': [6, [0.37647058823529411, 0.37647058823529411, 0.37647058823529411],12.0, 2.5666666666666669, 4.0, 4, 2.6000000000000001],
'Pd': [46, (1.0, 1.0, 1.0), 106.42, 4.3666666666666663, 1.0, 0, 2.2000000000000002],
'Cd': [48, (0.5, 0.29999999999999999, 0.0), 112.40000000000001, 4.9333333333333336, 1.0, 0, 1.7],
'Pm': [61, (1.0, 0.0, 0.69999999999999996), 146.90000000000001, 6.0333333333333332, 1.0, 0, 1.1000000000000001],
'Ho': [67, (1.0, 1.0, 0.0), 164.90000000000001, 5.8666666666666663, 1.0, 0, 1.2],
'Hf': [72, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 178.40000000000001, 5.0, 1.0, 0, 1.3],
'Hg': [80, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 200.5, 4.9666666666666668, 1.0, 0, 2.0],
'He': [2, (2.0, 0.69999999999999996, 0.69999999999999996), 4.0, 1.0666666666666667, 2.0, 2, 0],
'Mg': [12, (1.0, 1.0, 1.0), 24.300000000000001, 4.333333333333333, 2.0, 2, 1.3],
'K': [19, (0.59999999999999998, 0.0, 0.90000000000000002), 39.0, 6.5333333333333332, 1.0, 1, 0.80000000000000004],
'Mn': [25, (0.59999999999999998, 0.5, 0.59999999999999998), 55.0, 4.6333333333333337, 1.0, 0, 1.6000000000000001],
'O': [8, [0.91764705882352937, 0.0, 0.0],16.0, 2.4333333333333331, 6.0, 6, 3.3999999999999999],
'S': [16, (0.80000000000000004, 0.80000000000000004, 0.0), 32.0, 3.3999999999999999, 6.0, 6, 2.6000000000000001],
'W': [74, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 183.80000000000001, 4.8666666666666663, 1.0, 0, 2.3999999999999999],
'Zn': [30, (0.5, 0.5, 0.5), 65.400000000000006, 4.3666666666666663, 1.0, 0, 1.7],
'Eu': [63, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 151.90000000000001, 6.7999999999999998, 1.0, 0, 1.2],
'Er': [68, (1.0, 0.0, 0.69999999999999996), 167.19999999999999, 5.833333333333333, 1.0, 0, 1.2],
'Ni': [28, (0.5, 0.5, 0.5), 58.600000000000001, 4.0333333333333332, 1.0, 0, 1.8999999999999999],
'Na': [11, (1.0, 1.0, 0.0), 23.0, 5.1333333333333337, 1.0, 1, 0.90000000000000002],
'Nb': [41, (0.5, 0.5, 0.5), 92.0, 4.5666666666666664, 1.0, 0, 1.6000000000000001],
'Nd': [60, (0.69999999999999996, 0.0, 1.0), 144.0, 6.0333333333333332, 1.0, 0, 1.1000000000000001],
'Ne': [10, (2.0, 1.0, 0.0), 20.0, 2.2999999999999998, 8.0, 8, 0],
'Fe': [26, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 55.799999999999997, 4.166666666666667, 1.0, 0, 1.8],
'B': [5, [0.0, 0.44313725490196076, 0.0],10.800000000000001, 2.7333333333333334, 3.0, 3, 2.0],
'F': [9, [0.87450980392156863, 0.99215686274509807, 0.46666666666666667],19.0, 3.0, 7.0, 7, 4.0],
'Sr': [38, (0.90000000000000002, 0.29999999999999999, 0.0), 87.0, 4.2999999999999998, 2.0, 2, 0.90000000000000002],
'N': [7, (0.0, 0.0, 1.0), 14.0, 1.0, 5.0, 5, 3.0],
'Kr': [36, [0.27058823529411763, 0.9882352941176471, 0.91764705882352937],83.0, 3.6666666666666665, 8.0, 8, 0],
'Si': [14, (1.0, 0.90000000000000002, 0.90000000000000002), 28.0, 3.7000000000000002, 4.0, 4, 1.8999999999999999],
'Sn': [50, (0.40000000000000002, 0.40000000000000002, 0.5), 118.7, 4.7000000000000002, 4.0, 4, 2.0],
'Sm': [62, (1.0, 1.0, 0.0), 150.30000000000001, 6.0, 1.0, 0, 1.2],
'V': [23, (0.5, 0.59999999999999998, 0.59999999999999998), 51.0, 4.166666666666667, 1.0, 0, 1.6000000000000001],
'Sc': [21, (0.5, 0.5, 0.5), 45.0, 4.7999999999999998, 1.0, 0, 1.3999999999999999],
'Sb': [51, (0.69999999999999996, 0.80000000000000004, 1.0), 121.7, 4.5999999999999996, 5.0, 5, 2.1000000000000001],
'Se': [34, (0.0, 0.0, 0.5), 78.900000000000006, 3.8999999999999999, 6.0, 6, 2.6000000000000001],
'Co': [27, (0.69999999999999996, 0.5, 0.69999999999999996), 59.0, 4.2000000000000002, 1.0, 0, 1.8999999999999999],
'Cl': [17, (0.5, 1.0, 0.5), 35.0, 3.2999999999999998, 7.0, 7, 3.2000000000000002],
'Ca': [20, (1.0, 0.10000000000000001, 0.10000000000000001), 40.0, 5.7999999999999998, 2.0, 2, 1.0],
'Ce': [58, (0.90000000000000002, 0.90000000000000002, 0.90000000000000002), 140.0, 6.0666666666666664, 1.0, 0, 1.1000000000000001],
'Xe': [54, (1.0, 0.0, 2.0), 131.19999999999999, 4.333333333333333, 8.0, 8, 2.6000000000000001],
'Tm': [69, (0.0, 0.80000000000000004, 0.10000000000000001), 168.90000000000001, 5.7999999999999998, 1.0, 0, 1.3],
'Cs': [55, (0.69999999999999996, 0.5, 1.0), 132.90000000000001, 7.5, 1.0, 1, 0.80000000000000004],
'Cr': [24, (0.5, 0.69999999999999996, 0.5), 52.0, 4.2333333333333334, 1.0, 0, 1.7],
'Cu': [29, (0.0, 1.0, 1.0), 63.5, 4.5999999999999996, 1.0, 0, 2.0],
'La': [57, (0.90000000000000002, 0.90000000000000002, 0.90000000000000002), 138.90000000000001, 5.6333333333333337, 1.0, 0, 1.1000000000000001],
'Li': [3, (0.90000000000000002, 0.0, 0.90000000000000002), 6.9400000000000004, 4.4666666666666668, 1.0, 1],
'Tl': [81, (0.0, 0.5, 0.29999999999999999), 204.30000000000001, 4.9333333333333336, 3.0, 3, 2.0],
'Lu': [71, (0.90000000000000002, 0.90000000000000002, 0.90000000000000002), 174.90000000000001, 5.7999999999999998, 1.0, 0, 1.3],
'Ti': [22, (1.0, 1.0, 1.0), 47.799999999999997, 4.5333333333333332, 1.0, 0, 1.5],
'Te': [52, (0.80000000000000004, 0.80000000000000004, 0.84999999999999998), 127.0, 4.5, 6.0, 6, 2.1000000000000001],
'Tb': [65, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 158.90000000000001, 5.9333333333333336, 1.0, 0, 1.2],
'Tc': [43, (0.5, 0.5, 0.5), 97.0, 4.3666666666666663, 1.0, 0, 1.8999999999999999],
'Ta': [73, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 180.90000000000001, 4.5999999999999996, 1.0, 0, 1.5],
'Yb': [70, (0.90000000000000002, 0.90000000000000002, 0.90000000000000002), 173.0, 6.4333333333333336, 1.0, 0, 1.3],
'Dy': [66, (0.80000000000000004, 1.0, 0.0), 162.5, 5.9000000000000004, 1.0, 0, 1.2],
'I': [53, (0.80000000000000004, 0.29999999999999999, 0.90000000000000002), 126.90000000000001, 4.4333333333333336, 7.0, 7, 2.7000000000000002],
'Y': [39, (0.5, 0.5, 0.5), 88.900000000000006, 5.4000000000000004, 1.0, 0, 1.2],
'Ag': [47, (0.90000000000000002, 0.90000000000000002, 0.90000000000000002), 108.8, 5.0, 1.0, 0, 1.8999999999999999],
'Ir': [77, (0.80000000000000004, 0.80000000000000004, 0.80000000000000004), 192.0, 4.5666666666666664, 1.0, 0, 2.2000000000000002],
'Al': [13, (0.80000000000000004, 0.80000000000000004, 0.84999999999999998), 27.0, 3.9333333333333331, 3.0, 3, 1.6000000000000001],
'As': [33, (0.90000000000000002, 0.80000000000000004, 1.0), 74.900000000000006, 4.0333333333333332, 5.0, 5, 2.2000000000000002],
'Ar': [18, (0.20000000000000001, 0.80000000000000004, 2.0), 65.0, 3.2333333333333334, 8.0, 8, 0],
'Au': [79, (1.0, 0.80000000000000004, 0.0), 196.90000000000001, 4.7999999999999998, 1.0, 0, 2.5],
'Zr': [40, (0.59999999999999998, 0.59999999999999998, 0.59999999999999998), 91.200000000000003, 4.9333333333333336, 1.0, 0, 1.3],
'In': [49, (0.5, 0.0, 0.80000000000000004), 114.8, 4.7999999999999998, 3.0, 3, 1.8],
'Mo': [42, (0.59999999999999998, 0.59999999999999998, 0.59999999999999998), 95.900000000000006, 4.833333333333333, 1.0, 0, 2.2000000000000002]}
    f = file("atome.py","w")
    f.write("atomlist=" + str(atomlist))
    f.close()
def make_screenshot():
    img = ImageGrab.grab()
    d = os.getcwd() + "\\screenshots\\"
    d = asksaveasfilename()
    img.save(d,'PNG')
class AtomSlides(wx.Slider):
    def __init__(self, parent, id, maximum, setvalue, koor, name,func,vergleich=False):
        if vergleich:
            wx.Slider.__init__(self,parent,100,setvalue,0,maximum,koor,(111, -1),wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_TICKS)
        else:
            wx.Slider.__init__(self,parent,100,setvalue,0,maximum,koor,(180, -1),wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_TICKS)
        self.SetTickFreq(maximum/20., 0)
        if func:
            self.Bind(wx.EVT_SLIDER,func)
        wx.StaticText(parent, -1, name,  (koor[0]+8,koor[1]+35))
def vpythoncatch(vpython3,pos,name):
    scene2=display(title=name)
    scene2.exit=0
    scene2.select()
    scene2.visible=True
    VP = FindWindow ( None, name)
    if VP:
        flags = SWP_SHOWWINDOW or \
            SWP_FRAMECHANGED
        SetWindowPos( VP, HWND_TOPMOST,pos[0],pos[1],pos[2],pos[3], flags)
        SetParent (VP,vpython3.GetHandle ())
    return scene2,vpython3
class atomveraender(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1,"Atomdaten",size=(785,300),pos=(100,200))
        self.SetIcon(wx.Icon('Chythonicon.ico', wx.BITMAP_TYPE_ICO))
        self.Splitter=wx.SplitterWindow(self)
        self.panel=wx.Panel(self.Splitter,style=wx.BORDER_SUNKEN)
        self.vpython3=wx.Panel(self.Splitter,style=wx.BORDER_SUNKEN)
        self.Splitter.SplitVertically(self.panel,self.vpython3,185)
        atomewahl=wx.ListBox(self.panel, pos=(1,1),size=(-1,261),choices=namen)
        self.panel.Bind(wx.EVT_LISTBOX,self.atomonclick,atomewahl)
        farbebutton=wx.Button(self.panel, 1, "Farbe", (100, 10))
        self.panel.Bind(wx.EVT_BUTTON,self.atomonclickb,farbebutton)
        self.sliderveraender=wx.Slider(self.panel,10,100,10,100,(122,40), (-1, 170),wx.SL_VERTICAL | wx.SL_AUTOTICKS | wx.SL_SELRANGE)
        self.panel.Bind(wx.EVT_SLIDER,self.atomonclicks,self.sliderveraender)
        wx.StaticText(self.panel,pos=(122,210),label="Radius")
        speichern=wx.Button(self.panel, 2, "Speichern", (100, 232))
        self.panel.Bind(wx.EVT_BUTTON,self.atomonclicksave,speichern)
        self.vpython3.BackgroundColour="black"
        (self.scene2,self.vpython3)=vpythoncatch(self.vpython3,[295,-32,300,300],"Methanvergleich")
        syntuxzuatomzeichnen(self.scene2,["C",["H",[0,1,0]],["H",[0,1,0]],["H",[0,1,0]],["H",[0,1,0]]],0.5,1,1,10,1,1,self.vpython3,True)
        (self.scene2,self.vpython3)=vpythoncatch(self.vpython3,[-5,-32,305,300],"Vergleich")
    def atomonclick(self,a):
        for i in self.scene2.objects:
            i.visible=False
            del i
        self.nameumdenesgeht=name[namen[a.GetInt()]]
        atomumdasesgeht=eval("symbol"+self.nameumdenesgeht)
        self.sliderveraender.SetValue(atomumdasesgeht.radius*10)
        syntuxzuatomzeichnen(self.scene2,[self.nameumdenesgeht,["H",[0,1,0]],["H",[0,1,0]],["H",[0,1,0]],["H",[0,1,0]]],0.5,1,1,10,1,1,self.vpython3,True)
    def atomonclicks(self,a):
        wert=self.sliderveraender.GetValue()/10.
        for i in self.scene2.objects:
            if mag(i.pos)<0.1:
                i.radius=wert*0.5+1
                atomlist[self.nameumdenesgeht][3]=wert
                break
    def atomonclickb(self,a):
        clr=wx.ColourDialog(self.panel)
        if clr.ShowModal() == wx.ID_OK:
            clr=clr.GetColourData().GetColour().Get()
            bcolor=[clr[0]/255.,clr[1]/255.,clr[2]/255.]
            for i in self.scene2.objects:
                if mag(i.pos)<0.1:
                    i.color=bcolor
                    atomlist[self.nameumdenesgeht][1]=bcolor
    def atomonclicksave(self,a):
        f = file("atome.py","w")
        f.write("atomlist=" + str(atomlist))
class vergleichsfenster(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1,"Chython - Vergleichsfenster",size=(1024,738),pos=(0,0))
        self.SetIcon(wx.Icon('Chythonicon.ico', wx.BITMAP_TYPE_ICO))
        self.Splitter=wx.SplitterWindow(self,style=wx.SP_3DSASH|wx.SP_3DBORDER)
        projektionsflaeche1=wx.Panel(self.Splitter,-1,size=(512,738))
        projektionsflaeche2=wx.Panel(self.Splitter,-1,size=(512,738))
        self.Splitter.SplitVertically(projektionsflaeche1,projektionsflaeche2,512)
        MyMenu(self,-1,"chythonfenster1",True)
        MyMenu(self,-1,"chythonfenster2",True)
        VP = FindWindow ( None, "chythonfenster1")
        if VP:
            flags = SWP_SHOWWINDOW or \
                SWP_FRAMECHANGED
            SetWindowPos( VP, HWND_TOPMOST,-5,-32,525,738, flags)
            SetParent (VP,projektionsflaeche1.GetHandle ())
        VP = FindWindow ( None, "chythonfenster2")
        if VP:
            flags = SWP_SHOWWINDOW or \
                SWP_FRAMECHANGED
            SetWindowPos( VP, HWND_TOPMOST,-5,-32,525,738, flags)
            SetParent (VP,projektionsflaeche2.GetHandle ())
class datenbanken(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1,u"Datenbankeinträge",size=(500,300),pos=(100,200))
        self.SetIcon(wx.Icon('Chythonicon.ico', wx.BITMAP_TYPE_ICO))
        self.Splitter=wx.SplitterWindow(self)
        panel=wx.Panel(self.Splitter,style=wx.BORDER_SUNKEN)
        self.vpython3=wx.Panel(self.Splitter,style=wx.BORDER_SUNKEN)
        self.Splitter.SplitVertically(panel,self.vpython3,200)
        self.static1=wx.StaticText(panel,label=u"Präfix hier eingeben:",pos=(10,10))
        self.eingabe1=wx.TextCtrl(panel,-1,"", size=(180,-1),pos=(10,25),style=wx.TE_PROCESS_ENTER)
        self.static2=wx.StaticText(panel,label=u"SMILES hier eingeben:",pos=(10,55))
        self.eingabe2=wx.TextCtrl(panel,-1,"", size=(180,-1),pos=(10,70),style=wx.TE_PROCESS_ENTER)
        zeichnebutton=wx.Button(panel, 10, "Zeichnen", (10,100))
        belichtebutton=wx.Button(panel, 20, "Beleuchten", (115,100))
        speichern=wx.Button(panel, 30, "Speichern", (10,220))
        rb=wx.RadioBox(panel, -1, "Neuer Eintrag", (10,130), (180,-1),[u"Präfixe","Suffixe","Trivialnamen"], 1, wx.RA_SPECIFY_COLS)
        (self.scene2,self.vpython3)=vpythoncatch(self.vpython3,[-5,-32,300,300],"Datenbanktest")
        panel.Bind(wx.EVT_TEXT_ENTER,self.datenbankzeichne, self.eingabe2)
        panel.Bind(wx.EVT_BUTTON,self.datenbankzeichne, zeichnebutton)
        panel.Bind(wx.EVT_BUTTON,self.lichtvonvorne2, belichtebutton)
        panel.Bind(wx.EVT_BUTTON,self.speichereindatenbank, speichern)
        panel.Bind(wx.EVT_RADIOBOX,self.datenbankwechsel, rb)
        self.choice=0
    def lichtvonvorne2(self,a):
        angle=diff_angle2(-self.scene2.forward,self.scene2.lights[0].direction)
        axis=cross(-self.scene2.forward,self.scene2.lights[0].direction)
        self.scene2.lights[0].direction=rotate(self.scene2.lights[0].direction,angle,axis)
        self.scene2.lights[1].direction=rotate(self.scene2.lights[1].direction,angle,axis)
    def datenbankwechsel(self,a):
        self.choice=a.GetInt()
        if self.choice==0:
            self.static1.SetLabel(u"Präfix hier eingeben:")
            self.static2.SetLabel(u"SMILES hier eingeben:")
        elif self.choice==1:
            self.static1.SetLabel(u"Suffix hier eingeben:")
            self.static2.SetLabel(u"SMILES hier eingeben:")
        else:
            self.static1.SetLabel(u"Trivialnamen hier eingeben:")
            self.static2.SetLabel(u"IUPAC-Namen hier eingeben:")
    def SMILES_Convert3(self,i):
        if i=="":
            return ""
        bindung=1
        if i[0] in ("=","#"):
            bindung={"=":2,"#":3}[i[0]]
            i=i[1:]
        molekuel=smiles(i)
        bsch=molekuel.startconvert()
        for i2 in range(bindung):
            if ["H",[0,1,0]] in bsch:
                del bsch[bsch.index(["H",[0,1,0]])]
        bsch.insert(1,["@1C",[0,bindung,0]])
        return bsch
    def speichereindatenbank(self,a):
        entry=self.eingabe2.GetValue()
        entry=entry.replace(u"ä","ae").replace(u"ö","oe").replace(u"ü","ue").replace(u"ß","ss").replace("[","(").replace("]",")")
        name3=self.eingabe1.GetValue()
        name3=lower(name3.replace(u"ä","ae").replace(u"ö","oe").replace(u"ü","ue").replace(u"ß","ss").replace("[","(").replace("]",")"))
        name_db=["praefixe","suffixe","trivials"][self.choice]
        if self.choice in (0,1):
            datenbankpfad=getcwd()+"\\"+name_db+ ".py"
            entry=self.SMILES_Convert3(entry)
            if self.choice==0:
                entry[1]=[0,entry[1][1][1],0]
                praefix[str(name3)]=str(entry)
                file = open(datenbankpfad,"w")
                file.write("praefix="+str(praefix))
                file.close()
            else:
                zeichen=""
                for i in range(entry[1][1][1]):
                    zeichen+="+"
                entry[1]=zeichen
                entry=str(entry)
                entry=entry.replace("'",'"')
                suffix[str(name3)]=entry
                file = open(datenbankpfad,"w")
                file.write("suffix="+str(suffix))
                file.close()
        else:
            name3='"'+name3+'"'
            entry='"'+lower(entry)+'"'
            datenbankpfad=getcwd()+"\\trivials.csv"
            file = open(datenbankpfad,"r")
            hund = file.read()
            file.close()
            file = open(datenbankpfad,"w")
            file.write(hund+'\n'+name3+','+entry)
            file.close()
    def datenbankzeichne(self,a):
        for i in self.scene2.objects:
            i.visible=False
            del i
        (self.scene2,self.vpython3)=vpythoncatch(self.vpython3,[-5,-32,300,300],"Datenbanktest")
        molekuel=self.eingabe2.GetValue()
        if self.choice in (0,1):
            syntuxzuatomzeichnen(self.scene2,self.SMILES_Convert3(molekuel),0.5,1,1,10,1,1,self.vpython3,True)
        else:
            bsch=beschreibung(molekuel)
            syntuxzuatomzeichnen(self.scene2,bsch,0.5,1,1,10,1,1,self.vpython3,True)
def atomchange(panel):
    MyApp2(panel)
def datenbankchange(panel):
    MyApp3(panel)
def vergleichendesfenster(frame):
    MyVergleichsfensterApp(frame)
class MyApp2():
    def __init__(self,panel):
        frame = atomveraender(panel, -1,u"Chython Atome - Einstellungen verändern")
        frame.Show(True)
class MyApp3():
    def __init__(self,panel):
        frame = datenbanken(panel, -1,u"Chython Datenbanken - Einträge hinzufügen")
        frame.Show(True)
class MyApp3():
    def __init__(self,panel):
        frame = datenbanken(panel, -1,u"Chython Datenbanken - Einträge hinzufügen")
        frame.Show(True)
class MyVergleichsfensterApp():
    def __init__(self,parent):
        frame = vergleichsfenster(parent)
        frame.Show(True)
class FehlerApp():
    def __init__(self,panel):
        self.messagepanel=panel
    def Lokantenfehler(self,Worte):
        if len(Worte)==1:
            a=wx.MessageDialog(self.messagepanel,"Der Lokant des Substituentens "+Worte[0]+u" ist größer als die Stammgruppe.\nDieser Substituent wird nun nicht dargestellt",style=wx.ICON_INFORMATION)
        else:
            worte=Worte[0]
            for i in Worte[:-1]:
                worte+=" ,"+i
            worte+=" und "+Worte[-1]
            a=wx.MessageDialog(self.messagepanel,"Der Lokant der Substituenten "+Worte[0]+u" ist größer als die Stammgruppe.\nDiese Substituenten werden nun nicht dargestellt",style=wx.ICON_INFORMATION)
        a.ShowModal()
        a.Destroy
    def Endungsfehler(self,Worte):
        if len(Worte)==1:
            a=wx.MessageDialog(self.messagepanel,"Der Lokant der Endung "+Worte[0]+u" ist größer als die Stammgruppe.\nDiese Endungen wird nun nicht dargestellt",style=wx.ICON_INFORMATION)
        else:
            worte=Worte[0]
            for i in Worte[:-1]:
                worte+=" ,"+i
            worte+=" und "+Worte[-1]
            a=wx.MessageDialog(self.messagepanel,"Der Lokant der Endungen  "+Worte[0]+u" ist größer als die Stammgruppe.\nDiese Endungen werden nun nicht dargestellt",style=wx.ICON_INFORMATION)
        a.ShowModal()
        a.Destroy
    def Cyclofehlerzuklein(self,x):
        a=wx.MessageDialog(self.messagepanel,"Die Angabe 'cyclo' kann sich nicht wie angegeben auf ein system mit nur "+[1,"einem Ringatom","zwei Ringatomen"][x]+u" beziehen.\nAus diesem Grund wurde diese Angabe gelöscht",style=wx.ICON_INFORMATION)
        a.ShowModal()
        a.Destroy
    def Cyclofehler(self,x):
        a=wx.MessageDialog(self.messagepanel,"Die Darstellung von Ringen mit "+str(x)+u" Ringgliedern und den angegebenen Bindungen\nwird bisher noch nicht unterstützt. Das Ergebnis kann deshalb von anderen Modellen abweichen",style=wx.ICON_INFORMATION)
        a.ShowModal()
        a.Destroy
    def Boeseswort(self,x):
        if len(x)==1:
            message=u"Für den Wortteil '"+x[0]+"' konnte keine Bedeutung erkannt werden. Er wurde "
        else:
            boesemessage=""
            for i in x[-1]:
                boesemessage+="'"+i+"', "
            message=u"Für die Wortteile "+boesemessage+"und '"+x[-1]+"' konnten keine Bedeutungen erkannt werden. Sie wurden"
        a=wx.MessageDialog(self.messagepanel,message+u" deshalb gelöscht. Eventuell müssen Sie Präfixe, Suffixe oder Trivialnamen zur Datenbank hinzufügen",style=wx.ICON_INFORMATION)
        a.ShowModal()
        a.Destroy
class MyMenu(wx.Frame):
    def __init__(self, parent, id,title,vergleich=False):
        global fehlerapp
        wx.Frame.__init__(self, parent, id,title,(0,0), wx.Size(1024, 738))
        if vergleich:
            self.size=wx.Size(510, 738)
        #Fenster wird aufgeteilt, um spaeter ein VPythonfenster einbauen zu koennen
        self.SetIcon(wx.Icon('Chythonicon.ico', wx.BITMAP_TYPE_ICO))
        self.Show(False)
        self.Splitter=wx.SplitterWindow(self,style=wx.SP_3DBORDER|wx.SP_3DSASH)
        self.panel=wx.Panel(self.Splitter,style=wx.BORDER_SUNKEN)
        self.vpythonnotebook=wx.lib.agw.flatnotebook.FlatNotebook(self.Splitter,style=wx.NB_MULTILINE)
        if vergleich:
            self.Splitter.SplitHorizontally(self.vpythonnotebook,self.panel,400)
        else:
            self.Splitter.SplitVertically(self.panel,self.vpythonnotebook,424)
        self.vpython1=vpythonscene(self.vpythonnotebook,None)#wx.Panel(self.vpythonnotebook,style=wx.BORDER_SUNKEN)
        self.vpython=self.vpython1
        self.vpythonnotebook.AddPage(self.vpython1,"")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.notebookpagechanged,self.vpythonnotebook)
        self.vpython1.SetBackgroundColour("black")
        self.scene=display()
        self.numberofwindows=0
        ##hilfefenster(self.panel)
        #Menuleiste
        menubar=wx.MenuBar()
        bild         =wx.Menu()
        ansicht      =wx.Menu()
        einfugen     =wx.Menu()
        erweitern    =wx.Menu()
        atome        =wx.Menu()
        Hilfe        =wx.Menu()
        ezmw         =wx.Menu()#201
        griechisch   =wx.Menu()#301
        Pfix         =wx.Menu()#302
        Sfix         =wx.Menu()#303
        endungen     =wx.Menu()#304
        Sonderzeichen=wx.Menu()#305
        ersetzende   =wx.Menu()#306
        Tvial        =wx.Menu()#307
        atomemenu    =wx.Menu()#501
        bild.Append(101,"PNG-Export","Darstellung als .png-Datei exportieren")
        bild.Append(104,"SMILES-Export","Generieren des SMILES-Codes einer Darstellung")
        bild.Append(103,"SMILES-Import","Darstellung eines Molekuels durch Eingabe des SMILES-Code")
        bild.Append(105,"Vergleichendes Fenster",u"Fenster, indem zwei Moleküle gleichzeitig gezeigt werden können")
        bild.AppendSeparator()
        bild.Append(102,"Beenden"   ,"Chython beenden")
        self.Bind(wx.EVT_MENU,self.JPG_export,id=101)
        self.Bind(wx.EVT_MENU,self.SMILESConvert,id=103)
        self.Bind(wx.EVT_MENU,lambda a,i=self.panel:self.SMILESConvert2(i),id=104)
        self.Bind(wx.EVT_MENU,lambda a,i=self.panel:vergleichendesfenster(i),id=105)
        self.Bind(wx.EVT_MENU,self.CloseAll,id=102)
        ansicht.Append    (201,"Fullscreen","Darstellung auf Vollbildschirm",wx.ITEM_CHECK)
        ansicht.Append    (208,u"Bindungsgerüst","Bindungen bis zum Atomkern durchzeichnen", wx.ITEM_CHECK)
        ansicht.Append    (205,"Keil-Strich-Bindungen",u"polare Bindung als Keil darstellen",wx.ITEM_CHECK)
        ansicht.Append    (202,"Oxidationszahlen einblenden",u"Oxidationszahlen in Darstellung einblenden",wx.ITEM_CHECK)
        ansicht.Append    (203,"Elementsymbole einblenden",u"Elementsymbole in Darstellung einblenden",wx.ITEM_CHECK)
        ansicht.Append    (206,"Lokanten einblenden",u"Lokanten in Darstellung einblenden",wx.ITEM_CHECK)
        ansicht.Append    (204,"Hintergrundfarbe",u"Hintergrundfarbe der Darstellung wählen")
        ansicht.Append    (207,"Lichtfarbe",u"Lichtfarbe der Darstellung wählen")
        ansicht.Append    (209,u"Bindungen zu Wasserstoff",u"Abweichende Wasserstoffbindungen",wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.lokantenlabels,id=206)
        self.Bind(wx.EVT_MENU,self.keilstrich,id=205)
        self.Bind(wx.EVT_MENU,self.fullscreen,id=201)
        self.Bind(wx.EVT_MENU,self.oxidationszahl2,id=202)
        self.Bind(wx.EVT_MENU,self.elementsymbole,id=203)
        self.Bind(wx.EVT_MENU,self.backgcolor,id=204)
        self.Bind(wx.EVT_MENU,self.lichtcolor,id=207)
        self.Bind(wx.EVT_MENU,self.wasserstoff,id=209)
        self.Bind(wx.EVT_MENU_RANGE,self.bindungsgeruest,id=208)
        self.bcolor=(0,0,0)
        self.lcolor=(1,1,1)
        self.evtmenusonoff=[False,False,False,False,False,False]
        einfugen.AppendMenu(301,"Praefixe"                          ,Pfix        )
        einfugen.AppendMenu(302,"Suffixe"                           ,Sfix         )
        einfugen.AppendMenu(303,"weitere Endungen"                  ,endungen     )
        einfugen.AppendMenu(304,"Sonderzeichen"                     ,Sonderzeichen)
        einfugen.AppendMenu(305,"Kohlenstoff ersentzende"           ,ersetzende   )
        einfugen.AppendMenu(306,"Trivialnamen"                      ,Tvial        )
        einfugen.AppendMenu(307,"griechisches Alphabet"             ,griechisch   )
        erweitern.Append(401,"Datenbanken erweitern")
        self.Bind(wx.EVT_MENU,lambda a,panel=self.panel:datenbankchange(panel),id=401)
        atome.Append(501,u"Einstellungen ändern")
        self.Bind(wx.EVT_MENU,lambda a,panel=self.panel:atomchange(panel),id=501)
        Hilfe.Append(601,"Der einfache Gebrauch","allgemeine Informationen"               )
        Hilfe.AppendSeparator()
        Hilfe.Append(604,u"Über Chython","About")
        self.Bind(wx.EVT_MENU,self.about,id=604)
        self.Bind(wx.EVT_MENU,lambda a,i=self.panel:hilfefenster(i),id=601)
        self.greek3=[u'\N{GREEK SMALL LETTER ALPHA}',u'\N{GREEK SMALL LETTER BETA}',u'\N{GREEK SMALL LETTER GAMMA}',u'\N{GREEK SMALL LETTER DELTA}',u'\N{GREEK SMALL LETTER EPSILON}',u'\N{GREEK SMALL LETTER ZETA}',u'\N{GREEK SMALL LETTER ETA}',u'\N{GREEK SMALL LETTER THETA}',
        u'\N{GREEK SMALL LETTER IOTA}',u'\N{GREEK SMALL LETTER KAPPA}',u'\N{GREEK SMALL LETTER LAMDA}',u'\N{GREEK SMALL LETTER MU}',u'\N{GREEK SMALL LETTER NU}',u'\N{GREEK SMALL LETTER XI}',u'\N{GREEK SMALL LETTER OMICRON}',u'\N{GREEK SMALL LETTER PI}',u'\N{GREEK SMALL LETTER RHO}',
        u'\N{GREEK SMALL LETTER SIGMA}',u'\N{GREEK SMALL LETTER TAU}',u'\N{GREEK SMALL LETTER UPSILON}',u'\N{GREEK SMALL LETTER PHI}',u'\N{GREEK SMALL LETTER CHI}',u'\N{GREEK SMALL LETTER PSI}',u'\N{GREEK SMALL LETTER OMEGA}']
        self.greek4=['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa','Lambda', 'My', 'Ny', 'Xi', 'Omikron', 'Pi', 'Rho','Sigma', 'Tau', 'Ypsilon', 'Phi', 'Chi', 'Psi', 'Omega']
        for i in range(24):
            griechisch.Append(30801+i,self.greek3[i]+" - "+self.greek4[i],self.greek4[i]+u" hinzufügen")
            self.Bind(wx.EVT_MENU,lambda a,i=self.greek3[i]:self.hinzu(i), id=30801+i)
        p=praefix.keys()
        p.sort()
        for i in range(len(p)):
            Pfix.Append(30101+i,capitalize(p[i]),capitalize(p[i])+u" hinzufügen")
            self.Bind(wx.EVT_MENU,lambda a,i=p[i]:self.hinzu(i), id=30101+i)
        p=suffix.keys()
        p.sort()
        for i in range(len(p)):
            Sfix.Append(30201+i,p[i],p[i]+u" hinzufügen")
            self.Bind(wx.EVT_MENU,lambda a,i=p[i]:self.hinzu(i), id=30201+i)
        p=['al','at', 'amid', 'an','aza','azano', 'en', 'in','o', 'oat', 'ol', 'on','oxy', 'oyl', 'saeure', 'saeureanhydrid', 'yl', 'ylen', 'yliden', 'ylidin', 'ylin']
        for i in range(21):
            endungen.Append(30301+i,p[i],"'"+p[i]+u"' hinzufügen")
            self.Bind(wx.EVT_MENU,lambda a,i=p[i]:self.hinzu(i), id=30301+i)
        p=["bi","cis","cyclo","per","(r)","(s)","trans"]
        for i in range(7):
            Sonderzeichen.Append(30401+i,p[i],"'"+p[i]+u"' hinzufügen")
            self.Bind(wx.EVT_MENU,lambda a,i=p[i]:self.hinzu(i), id=30401+i)
        p=['arsa', 'aza', 'bisma', 'bora', 'broma', 'chlora', 'fluora', 'germa', 'ioda', 'mercura', 'oxa', 'phospha', 'plumba', 'selena', 'sila', 'stanna', 'stiba', 'tellura', 'thia']
        for i in range(19):
            ersetzende.Append(30501+i,p[i],p[i]+u" hinzufügen")
            self.Bind(wx.EVT_MENU,lambda a,i=p[i]:self.hinzu(i),id=30501+i)
        rows2=[]
        reader=csv.reader(open("trivials.csv","rb"),delimiter=",")
        for row in reader:
            rows2.append(capitalize(row[0]))
        rows2.sort()
        i=0
        for rows in rows2:
            Tvial.Append(30601+i,rows,rows+u" hinzufügen")
            self.Bind(wx.EVT_MENU,lambda a,i=rows:self.hinzu(i), id=30601+i)
            i+=1
        menubar.Append(bild,"Datei")
        menubar.Append(ansicht,"Ansicht")
        menubar.Append(einfugen,u"Einfügen")
        menubar.Append(erweitern,"Datenbanken erweitern")
        menubar.Append(atome,"Atome")
        menubar.Append(Hilfe,"Hilfe")
        self.SetMenuBar(menubar)
        ##Oberflaeche
        unicodestring=u"Neues Molekül"
        if vergleich:
            wx.StaticBox(self.panel,-1,unicodestring,pos=(5,8),size=(485,99))
            wx.StaticText(self.panel,label="IUPAC-Nomenklaturname hier eingeben:",pos=(19,25))
            self.eingabe = wx.SearchCtrl(self.panel,-1,"", size=(280,-1),pos=(14,40),style=wx.TE_PROCESS_ENTER)
            self.eingabe.SearchButtonVisible=False
            self.eingabe.CancelButtonVisible=True
            zeichnebutton     = wx.Button(self.panel, 10, "Zeichnen", (14,70))
            lichtbutton     = wx.Button(self.panel, 20, "Beleuchten", (110,70))
            self.mittelpunktbutton = False
            self.panel.Bind(wx.EVT_TEXT_ENTER,lambda i:self.zeichne(self.eingabe.GetValue(),vergleich=True), self.eingabe)
            self.panel.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,self.eingabeloesch,self.eingabe)
            self.panel.Bind(wx.EVT_BUTTON,lambda i:self.zeichne(self.eingabe.GetValue(),vergleich=True),zeichnebutton)
            self.panel.Bind(wx.EVT_BUTTON,self.lichtvonvorne,lichtbutton)
            self.slider_z=wx.Slider(self.panel,3001,0,-50,50,(380,15),(80, -1),wx.SL_HORIZONTAL)
            self.slider_y=wx.Slider(self.panel,3003,0,-50,50,(380,80),(80, -1),wx.SL_TOP)
            self.slider_x=wx.Slider(self.panel,3002,0,-50,50,(455,18),(-1, 80),wx.SL_VERTICAL|wx.SL_LEFT)
            self.Bind(wx.EVT_SLIDER,self.drehstart,self.slider_x)
            self.Bind(wx.EVT_SLIDER,self.drehstart,self.slider_y)
            self.Bind(wx.EVT_SLIDER,self.drehstart,self.slider_z)
            self.Bind(wx.EVT_SCROLL_ENDSCROLL,self.dreheende,self.slider_x)
            self.Bind(wx.EVT_SCROLL_ENDSCROLL,self.dreheende,self.slider_y)
            self.Bind(wx.EVT_SCROLL_ENDSCROLL,self.dreheende,self.slider_z)
            unicodestring=u"Bindungslänge"
            unicodestring2=u"Lichtintensität"
            box = wx.StaticBox(self.panel, -1, "Darstellungsbearbeitung",pos=(5,116),size=(485,300))
            self.slider11 = AtomSlides(self.panel,11,100,30, (13,136),"Atomproportion"    ,self.slider11neu,True)
            self.slider12 = AtomSlides(self.panel,12,100,10, (13,206),"Atomradius"        ,self.slider11neu,True)
            self.slider13 = AtomSlides(self.panel,13,100,50, (132,136),"Bindungsradius"    ,self.slider13neu,True)
            self.slider14 = AtomSlides(self.panel,14,100,10, (132,206),unicodestring    ,False,True)
            self.slider21 = AtomSlides(self.panel,21,100,100,(251,136),"Kugeltransparenz",self.slider21neu,True)
            self.slider22 = AtomSlides(self.panel,22,100,100,(251,206),"Stabtransparenz" ,self.slider22neu,True)
            self.slider23 = AtomSlides(self.panel,23,10,1,   (370,136),"Repetiereinheiten"  ,self.bttiefe,True)
            self.slider25 = AtomSlides(self.panel,25,100,30, (370,206),unicodestring2,self.slider25neu,True)
            sampleList=["","","","","",""]
            self.rb = wx.RadioBox(self.panel, -1, "",(0,0), size=(0,0),choices=sampleList, majorDimension=1)
            self.rb.SetSelection(5)
        else:
            wx.StaticBox(self.panel,-1,unicodestring,pos=(10,8),size=(401,99))
            wx.StaticText(self.panel,label="IUPAC-Nomenklaturname hier eingeben:",pos=(19,25))
            self.eingabe = wx.SearchCtrl(self.panel,-1,"", size=(280,-1),pos=(19,40),style=wx.TE_PROCESS_ENTER)
            self.eingabe.SearchButtonVisible=False
            self.eingabe.CancelButtonVisible=True
            zeichnebutton     = wx.Button(self.panel, 10, "Zeichnen", (19,70))
            lichtbutton     = wx.Button(self.panel, 20, "Beleuchten", (115,70))
            self.mittelpunktbutton = False
            self.panel.Bind(wx.EVT_TEXT_ENTER,lambda i:self.zeichne(self.eingabe.GetValue()), self.eingabe)
            self.panel.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,self.eingabeloesch,self.eingabe)
            self.panel.Bind(wx.EVT_BUTTON,lambda i:self.zeichne(self.eingabe.GetValue()),zeichnebutton)
            self.panel.Bind(wx.EVT_BUTTON,self.lichtvonvorne,lichtbutton)
            self.slider_z=wx.Slider(self.panel,3001,0,-50,50,(300,15),(80, -1),wx.SL_HORIZONTAL)
            self.slider_y=wx.Slider(self.panel,3003,0,-50,50,(300,80),(80, -1),wx.SL_TOP)
            self.slider_x=wx.Slider(self.panel,3002,0,-50,50,(370,18),(-1, 80),wx.SL_VERTICAL|wx.SL_LEFT)
            self.Bind(wx.EVT_SLIDER,self.drehstart,self.slider_x)
            self.Bind(wx.EVT_SLIDER,self.drehstart,self.slider_y)
            self.Bind(wx.EVT_SLIDER,self.drehstart,self.slider_z)
            self.Bind(wx.EVT_SCROLL_ENDSCROLL,self.dreheende,self.slider_x)
            self.Bind(wx.EVT_SCROLL_ENDSCROLL,self.dreheende,self.slider_y)
            self.Bind(wx.EVT_SCROLL_ENDSCROLL,self.dreheende,self.slider_z)
            unicodestring=u"Bindungslänge"
            unicodestring2=u"Lichtintensität"
            box = wx.StaticBox(self.panel, -1, "Darstellungsbearbeitung",pos=(10,116),size=(401,300))
            self.slider11 = AtomSlides(self.panel,11,100,30, (13,136),"Atomproportion"    ,self.slider11neu)
            self.slider12 = AtomSlides(self.panel,12,100,10, (228,136),"Atomradius"        ,self.slider11neu)
            self.slider13 = AtomSlides(self.panel,13,100,50, (13,206),"Bindungsradius"    ,self.slider13neu)
            self.slider14 = AtomSlides(self.panel,14,100,10, (228,206),unicodestring    ,False)
            self.slider21 = AtomSlides(self.panel,21,100,100,(13,276),"Kugeltransparenz",self.slider21neu)
            self.slider22 = AtomSlides(self.panel,22,100,100,(228,276),"Stabtransparenz" ,self.slider22neu)
            self.slider23 = AtomSlides(self.panel,23,10,1,   (13,346),"Repetiereinheiten"  ,self.bttiefe)
            self.slider25 = AtomSlides(self.panel,25,100,30, (228,346),unicodestring2,self.slider25neu)
            sampleList=[" Kalottenmodell 1   "," Kugel-Stab-Modell 1   ",u" Stäbchenmodell    "," Kalottenmodell 2   "," Kugel-Stab-Modell 2   "," Benutzerdefiniert    "]
            self.rb = wx.RadioBox(self.panel, -1, "Voreinstellungen",(10,425), size=(-1,-1),choices=sampleList, majorDimension=3, style=wx.RA_SPECIFY_COLS)
            self.rb.SetSelection(4)
            self.panel.Bind(wx.EVT_RADIOBOX,self.setvisualisationmode, self.rb)
            font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
            unicodestring=u"Molekülinformationen"
            box = wx.StaticBox(self.panel, -1, unicodestring,pos=(10,497),size=(401,160))
            self.text1=wx.StaticText(self.panel,-1,"Name",pos=(30,528))
            self.text1.SetFont(font)
            self.text2=wx.StaticText(self.panel,-1,"Summenformel",pos=(30,568))
            self.text2.SetFont(font)
            self.text3=wx.StaticText(self.panel,-1,"Molare Masse",pos=(30,608))
            self.text3.SetFont(font)
            self.textname        =wx.StaticText(self.panel,-1,": ",pos=(190,528))
            self.textname.SetFont(font)
            self.textsummenformel=wx.StaticText(self.panel,-1,": ",pos=(190,568))
            self.textsummenformel.SetFont(font)
            self.textmolare_masse=wx.StaticText(self.panel,-1,": ",pos=(190,608))
            self.textmolare_masse.SetFont(font)
            self.timer2=wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.entdecke,self.timer2)
        self.bindungsg=False
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.drehe,self.timer)
        #Eine Fehlerapp wird vorbereitet
        fehlerapp=FehlerApp(self.panel)
    def CloseAll(self,evt):
        self.Close()
    def SMILESConvert(self,a):
        dlg = wx.TextEntryDialog(self.vpython, 'SMILES-Code','SMILES-Import')
        if dlg.ShowModal() == wx.ID_OK:
            self.zeichne(dlg.GetValue(),SMILES=True)
        dlg.Destroy()
    def SMILESConvert2(self,vpython):
        dlg = wx.MessageDialog(vpython, "Der SMILES-Code lautet "+startconvert2(self.bsch),'SMILES Export',wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    def zeichne(self,a,SMILES=False,vergleich=False):
        if a=="":
            return
        self.sza=[]
        if SMILES:
            molekuel=smiles(a)
            self.bsch=molekuel.startconvert()
            a2=oldcopy.copy(a)
        else:
            a2=a.replace(u"ä","ae").replace(u"ö","oe").replace(u"ü","ue").replace(u"ß","ss").replace("[","(").replace("]",")")
            self.bsch=beschreibung(a2)
            for i in range(len(a)):
                if a[i] in letters:
                    a=a[:i]+upper(a[i])+a[i+1:]
                    break
            for i in range(len(a2)):
                if a2[i] in self.greek3:
                    a2=a2[:i]+lower(self.greek4[self.greek3.index(a2[i])])+a2[i+1:]
        if not vergleich:
            summenformel=self.formel()
            self.textname.        SetLabel(": "+a)
            self.textsummenformel.SetLabel(": "+summenformel[0])
            self.textmolare_masse.SetLabel(": "+str(summenformel[1])+" g/mol")
        darstellungsname=str("Darstellung"+a2)
        scene=display(title=darstellungsname,x=434,y=78,exit=0,visible=0,fullscreen=self.evtmenusonoff[0],ambient=.5,background=self.bcolor)
        scene.select()
        self.numberofwindows+=1
        if self.numberofwindows==1:
            self.vpythonnotebook.DeleteAllPages()
        exec("self.vpython"+str(self.numberofwindows)+"=vpythonscene(self.vpythonnotebook,scene)")
        self.vpythonnotebook.AddPage(eval("self.vpython"+str(self.numberofwindows)),a,select=True)
        self.current=self.vpythonnotebook.GetCurrentPage()
        self.current.SetBackgroundColour("black")
        self.sza=syntuxzuatomzeichnen(self.current.scene,self.bsch,self.slider12.GetValue()/20.,self.slider13.GetValue()/50.,self.slider11.GetValue()/30.,self.slider14.GetValue(),self.slider21.GetValue()/100.,self.slider22.GetValue()/100.,self.current,self.bindungsg,self.evtmenusonoff[3],self.evtmenusonoff[5])
        self.scene.visible=True
        if not self.evtmenusonoff[0]:
            VP = FindWindow ( None, darstellungsname)
            if VP:
                flags = SWP_SHOWWINDOW or \
                    SWP_FRAMECHANGED
                if vergleich:
                    SetWindowPos( VP, HWND_TOPMOST,-5,-32,508,410, flags)
                else:
                    SetWindowPos( VP, HWND_TOPMOST,-5,-32,594,720, flags)
                SetParent (VP,self.current.GetHandle ())
            if a=="#":
                return
        self.Show(True)
        self.SetTitle("Chython: "+str(a2))
        for i in range(len(self.sza[0])):
            self.sza[0][i]=ohnezahlen(self.sza[0][i])
        self.current.setsza(self.sza)
        gesamtpos=vector(0,0,0)
        gesamtaxis=vector(0,0,0)
        for i in self.sza[1]:
            gesamtpos+=i.pos
        for i in self.sza[1]:
            gesamtaxis+=norm(i.pos-gesamtpos)
        self.scene.center=gesamtpos/len(self.sza[1])
        winkel=diff_angle(-self.scene.forward,gesamtaxis)
        achse=cross(-self.scene.forward,gesamtaxis)
        self.scene.forward=-rotate(-self.scene.forward,winkel,achse)
        self.scene.up=rotate(self.scene.up,winkel,achse)
        self.scene.forward=rotate(self.scene.forward,pi/2,self.scene.up)
        if self.evtmenusonoff[1]:
            roemisch=["0","I","II","III","IV","V","VI","VII","VIII"]
            for i in range(len(self.sza[2])):
                if self.sza[2][i]==-10:
                    continue
                text=roemisch[absolute(self.sza[2][i])]
                if self.sza[2][i]<0:
                    text="-"+text
                label(text=text,pos=self.sza[1][i].pos,linecolor=self.sza[1][i].color)
        elif self.evtmenusonoff[2]:
            for i in range(len(self.sza[2])):
                text=self.sza[0][i]
                if text=="xx":
                    continue
                label(text=text,pos=self.sza[1][i].pos,linecolor=self.sza[1][i].color)
        elif self.evtmenusonoff[4]:
            for i in range(len(self.sza[3])):
                if self.sza[3][i]!="":
                    label(text=self.sza[3][i],pos=self.sza[1][i].pos,linecolor=self.sza[1][i].color)
        if not self.mittelpunktbutton and not vergleich:
            self.mittelpunktbutton=wx.Button(self.panel, 30, u"Atom anwählen", (208,70))
            self.panel.Bind(wx.EVT_BUTTON,self.TimerStart,self.mittelpunktbutton)
        self.slider25neu(1)
        for i in range(len(self.sza[0])):
            if self.sza[0][i]=="xx":
                self.sza[1][i].visible=False
        if self.evtmenusonoff[0]:
            self.scene.visible=True
            self.scene.userspin=False
            while 1:
                if scene.kb.keys: # is there an event waiting to be processed?
                    s = scene.kb.getkey() # obtain keyboard information
                    if s=="up":
                        self.drehe([0,0,10])
                    elif s=="down":
                        self.drehe([0,0,-10])
                    elif s=="left":
                        self.drehe([0,-10,0])
                    elif s=="right":
                        self.drehe([0,10,0])
                    elif s=="shift+left":
                        self.drehe([-10,0,0])
                    elif s=="shift+right":
                        self.drehe([10,0,0])
                    elif s=="escape":
                        break
                    elif s=="1":
                        break
    def entdecke(self,a):
        if self.scene.mouse.events:
            m=self.scene.mouse.getclick()
            atom=m.pick
            if atom.__class__==sphere:
                self.TimerStop()
                indexatom=self.sza[1].index(atom)
                self.text1.SetLabel("Element")
                self.text2.SetLabel("Oxidationszahl")
                if self.sza[3][indexatom]=="":
                    self.text3.SetLabel("")
                else:
                    self.text3.SetLabel("Lokant")
                self.newcenter=wx.Button(self.panel,pos=[321,608],label="Als Mittelpunkt")
                self.panel.Bind(wx.EVT_BUTTON,lambda a,i=indexatom:self.setCenter(i),self.newcenter)
                self.backbutton=wx.Button(self.panel,pos=[321,632],label=u"Zurück",size=self.newcenter.GetSize())
                self.panel.Bind(wx.EVT_BUTTON,self.textschreiber,self.backbutton)
                self.texte=(self.textname.GetLabel(),self.textsummenformel.GetLabel(),self.textmolare_masse.GetLabel())
                self.textname.SetLabel(self.sza[0][indexatom]+" , "+name.keys()[name.values().index(self.sza[0][indexatom])])
                self.textsummenformel.SetLabel(str(self.sza[2][indexatom]))
                self.textmolare_masse.SetLabel(str(self.sza[3][indexatom]))
    def setCenter(self,i):
        self.scene.center=(self.sza[1][i].pos)
    def textschreiber(self,a):
        self.text1.SetLabel("Name")
        self.text2.SetLabel("Summenformel")
        self.text3.SetLabel("Molare Masse")
        self.textname.SetLabel(self.texte[0])
        self.textsummenformel.SetLabel(self.texte[1])
        self.textmolare_masse.SetLabel(self.texte[2])
        del self.texte
        self.newcenter.Destroy()
        self.backbutton.Destroy()
    def TimerStart(self,a):
        if not self.timer2.IsRunning():
            self.timer2.Start(100)
    def TimerStop(self):
        self.timer2.Stop()
    def JPG_export(self,a):
        wildcard = "Portable Network Graphic (*.png)|*.png"
        dlg = wx.FileDialog(
            self.panel, message="Bild speichern",defaultDir=os.getcwd(),defaultFile="",wildcard=wildcard,style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()[0]
            im = ImageGrab.grab((434,78,1018,734))
            im.save(paths)
    def backgcolor(self,a):
        clr=wx.ColourDialog(self.panel)
        if clr.ShowModal() == wx.ID_OK:
            clr=clr.GetColourData().GetColour().Get()
            self.bcolor=[clr[0]/255.,clr[1]/255.,clr[2]/255.]
            self.scene.background=self.bcolor
    def lichtcolor(self,a):
        clr=wx.ColourDialog(self.panel)
        if clr.ShowModal() == wx.ID_OK:
            clr=clr.GetColourData().GetColour().Get()
            self.lcolor=[clr[0]/255.,clr[1]/255.,clr[2]/255.]
            for i in self.scene.lights:
                i.color=self.lcolor
    def wasserstoff(self,a):
        if self.evtmenusonoff[5]==True:
            self.evtmenusonoff[5]=False
        else:
            self.evtmenusonoff[5]=True
    def lichtvonvorne(self,a):
        angle=diff_angle2(-self.scene.forward,self.scene.lights[0].direction)
        axis=cross(-self.scene.forward,self.scene.lights[0].direction)
        self.scene.lights[0].direction=rotate(self.scene.lights[0].direction,angle,axis)
        self.scene.lights[1].direction=rotate(self.scene.lights[1].direction,angle,axis)
        self.slider25neu(1)
    def hinzu(self,a):
        ip=self.eingabe.InsertionPoint
        gv=self.eingabe.GetValue()
        self.eingabe.SetValue(gv[:ip]+a+gv[ip:])
        self.eingabe.SetInsertionPoint(len(self.eingabe.GetValue()))
    def slider13neu(self,a):
        if self.rb.GetSelection!=5 and a:
            self.rb.SetSelection(5)
        for i in self.scene.objects:
            if i.__class__==cylinder or i.__class__==cone:
                i.radius=self.slider13.GetValue()/50.
            elif i.__class__==curve:
                i.radius=(self.slider13.GetValue()-1)/50.
    def slider11neu(self,a):
        if self.rb.GetSelection!=5 and a:
            self.rb.SetSelection(5)
        for i in range(len(self.sza[0])):
            if self.sza[0][i]=="xx":
                continue
            self.sza[1][i].radius=eval("symbol"+self.sza[0][i]).radius*self.slider12.GetValue()/20.+self.slider11.GetValue()/30.
    def slider21neu(self,a):
        for i in range(len(self.sza[0])):
            if self.sza[0][i]=="xx":
                continue
            self.sza[1][i].opacity=self.slider21.GetValue()/100.
    def slider22neu(self,a):
        for i in self.scene.objects:
            if i.__class__==cylinder:
                i.opacity=self.slider22.GetValue()/100.
    def slider25neu(self,a):
        self.scene.ambient=self.slider25.GetValue()/50.
        for i in range(len(self.scene.lights)):
            faktor=(self.slider25.GetValue()+1)/max(self.scene.lights[i].color)/50.
            self.scene.lights[i].color=(self.scene.lights[i].color[0]*faktor,self.scene.lights[i].color[1]*faktor,self.scene.lights[i].color[2]*faktor)
    def setvisualisationmode(self,event):
        choice=event.GetInt()
        if choice==0:
            choice2=[50,80,0,10]
        if choice==3:
            choice2=[100,60,0,10]
        if choice==1:
            choice2=[24,20,80,10]
        if choice==4:
            choice2=[30,10,50,10]
        if choice==2:
            choice2=[30,0,50,10]
        self.slider11.SetValue(choice2[0])
        self.slider12.SetValue(choice2[1])
        self.slider13.SetValue(choice2[2])
        self.slider14.SetValue(choice2[3])
        self.slider11neu(False)
        self.slider13neu(False)
    def formel(self):
        masse=0
        a=summenformel2(self.bsch)
        summenformel3=""
        if "C" in a.keys():
            summenformel3+="C"+dazu3(a["C"])
            masse+=info("atom","C")[2]*a["C"]
            del a["C"]
            if "H" in a.keys():
                summenformel3+="H"+dazu3(a["H"])
                masse+=info("atom","H")[2]*a["H"]
                del a["H"]
        a1=a.keys()
        a1.sort()
        for i in a1:
            summenformel3+=i+dazu3(a[i])
            masse+=info("atom",i)[2]*a[i]
        return summenformel3,masse
    def about(self,i):
        info = wx.AboutDialogInfo()
        info.Name = u"Chython - digitales Molekülmodell"
        info.Version = "1.0"
        info.Copyright = u"(C) 2009 Stefan Mühlbauer und Ben Heuer"
        info.Description = wordwrap(
            u"Chython ist ein Programm zur räumlichen Darstellung von Molekülen,"
            u" das den Aufbau des Moleküls nicht durch Datenbankabgleich ermittelt,"
            " sondern seine Struktur durch Analyse des IUPAC-Nomenklaturnamens errechnet"

            u"\n\nDiese Besonderheit führt zu einem besonders hohen Maß an Flexibilität,"
            " die durch Datenbanken nicht erreicht werden kann."
            "\n\nChython ist entstanden im Rahmen des \n\"Jugend forscht\"-Wettbewerbs 2009"
            " und wurde beim Bundeswettbewerb mit einem zweiten Platz ausgezeichnet.",
            350, wx.ClientDC(self.panel))
        info.WebSite = ("http://www.chython.de", "Chython Homepage")
        info.Developers = [ u"Stefan Mühlbauer","Ben Heuer"]
        info.License = ""
        wx.AboutBox(info)
    def bttiefe(self,a):
        global mi
        mi=self.slider23.GetValue()
    def bindungsgeruest(self,i):
        if self.bindungsg:
            self.bindungsg=False
        else:
            self.bindungsg=True
    def fullscreen(self,a):
        if self.evtmenusonoff[0]==True:
            self.evtmenusonoff[0]=False
        else:
            self.evtmenusonoff[0]=True
    def lokantenlabels(self,a):
        if self.evtmenusonoff[4]==True:
            self.evtmenusonoff[4]=False
            for i in self.scene.objects:
                if i.__class__==label:
                    i.visible=False
        else:
            self.evtmenusonoff[4]=True
            for i in range(len(self.sza[3])):
                if self.sza[3][i]!="":
                    label(text=self.sza[3][i],pos=self.sza[1][i].pos,linecolor=self.sza[1][i].color)
    def keilstrich(self,a):
        if self.evtmenusonoff[3]==True:
            self.evtmenusonoff[3]=False
        else:
            self.evtmenusonoff[3]=True
    def oxidationszahl2(self,a):
        for i in self.scene.objects:
                if i.__class__==label:
                    i.visible=False
        if self.evtmenusonoff[1]==True:
            self.evtmenusonoff[1]=False
        else:
            self.evtmenusonoff[1]=True
            roemisch=["0","I","II","III","IV","V","VI","VII","VIII"]
            for i in range(len(self.sza[2])):
                if self.sza[2][i]==-10:
                    continue
                text=roemisch[absolute(self.sza[2][i])]
                if self.sza[2][i]<0:
                    text="-"+text
                label(text=text,pos=self.sza[1][i].pos,linecolor=self.sza[1][i].color)
    def elementsymbole(self,a):
        for i in self.scene.objects:
                if i.__class__==label:
                    i.visible=False
        if self.evtmenusonoff[2]==True:
            self.evtmenusonoff[2]=False
        else:
            self.evtmenusonoff[2]=True
            for i in range(len(self.sza[2])):
                text=self.sza[0][i]
                if text=="xx":
                    continue
                label(text=text,pos=self.sza[1][i].pos,linecolor=self.sza[1][i].color)
    def notebookpagechanged(self,a):
        self.vpython=self.vpythonnotebook.GetCurrentPage()
        self.scene=self.vpython.scene
        self.sza=self.vpython.sza
    def drehe(self,a):
        if type(a)==list:
            x,y,z=a
        else:
            x=self.slider_x.GetValue()
            y=self.slider_y.GetValue()
            z=self.slider_z.GetValue()
        zachse=-self.scene.forward
        yachse=self.scene.up
        xwinkel=diff_angle2(zachse,yachse)
        if xwinkel<.1:
            xachse=(-1,0,0)
        elif xwinkel>3.1415:
            xachse=(1,0,0)
        else:
            xachse=cross(yachse,zachse)
        if x:
            self.scene.forward=-rotate(-self.scene.forward,radians(x/-20.),xachse)
            self.scene.up=rotate(self.scene.up,radians(x/-20.),xachse)
        elif y:
            self.scene.forward=-rotate(-self.scene.forward,radians(y/-20.),yachse)
        elif z:
            self.scene.up=rotate(self.scene.up,radians(z/20.),zachse)
    def dreheende(self,a):
        self.slider_x.SetValue(0)
        self.slider_y.SetValue(0)
        self.slider_z.SetValue(0)
        self.timer.Stop()
    def drehstart(self,a):
        if not self.timer.IsRunning():
            if self.slider_x.GetValue()!=0 or self.slider_y.GetValue()!=0 or self.slider_z.GetValue()!=0:
                self.timer.Start(10)
    def eingabeloesch(self,a):
        self.eingabe.SetValue("")
class MyApp(wx.App):
    def OnInit(self):
        frame=MyMenu(None, -1, 'Chython.py')
        frame=frame.Show(True)
        return True
class Hilfefenster(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,-1,"Hilfe",size=(636,406))
        self.SetIcon(wx.Icon('Chythonicon.ico', wx.BITMAP_TYPE_ICO))
        self.Show(False)
        self.Splitter=wx.SplitterWindow(self)
        self.treepanel=wx.Panel(self.Splitter,style=wx.BORDER_SUNKEN)
        self.panelpanel=wx.Panel(self.Splitter,style=wx.BORDER_SUNKEN)
        self.Splitter.SplitVertically(self.treepanel,self.panelpanel,300)
        self.tree = wx.TreeCtrl(self.treepanel,10,pos=(10,10),size=(280,350),style =wx.TR_DEFAULT_STYLE| wx.TR_FULL_ROW_HIGHLIGHT)
        self.textctrl =wx.TextCtrl(self.panelpanel, -1,pos=(10,10),size=(300, 350), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.Gebrauch =self.tree.AddRoot("Der einfache Gebrauch")
        self.namen=[u"Ein Molekül zeichnen lassen",u"Einstellungen für das Molekül treffen",u"Einstellungen für weitere Darstellung","Import/Export-Funktionen",u"Erweiterung der Möglichkeiten","Konfiguration der Atomdaten","Drehen der Darstellung"]
        self.gebrauch1=self.tree.AppendItem(self.Gebrauch,self.namen[0])
        self.gebrauch2=self.tree.AppendItem(self.Gebrauch,self.namen[1])
        self.gebrauch3=self.tree.AppendItem(self.Gebrauch,self.namen[2])
        self.gebrauch4=self.tree.AppendItem(self.Gebrauch,self.namen[3])
        self.gebrauch5=self.tree.AppendItem(self.Gebrauch,self.namen[4])
        self.gebrauch6=self.tree.AppendItem(self.Gebrauch,self.namen[5])
        self.gebrauch7=self.tree.AppendItem(self.Gebrauch,self.namen[6])
        self.tree.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDClick)
        self.Show(True)
        self.text1=u"Ein Molekül zeichnen lassen: Geben sie den rationellen Namen eines Moleküls gemäß der IUPAC-Nomenklatur im Eingabefenster ein und drücken sie auf [Zeichnen], das dreidimensionale Modell erscheint. Bei dem nächsten Molekül bleibt das vorherige vorhanden, sie können es über "+u"die Tableiste über den einzelnen Molekülen auswählen."
        self.text2=u"Auf der linken Seite finden sie eine Vielzahl an Schiebereglern, die es Ihnen ermöglichen, die momentane Darstellung des Moleküls zu variieren. Über den Atomradius bzw. die Atomproportion ändern sie die Größer der Atome, über den Bindungsradius und die Bindungslänge (erst "+u"beim nächsten Zeichnen sichtbar) die Bindungen. Des Weiteren können sie Transparenz vonAtomen und Bindungen variieren sowie die Genauigkeit der Berechnung einstellen. Um eine entsprechende Beleuchtung zu ändern nutzen sie die Lichtintensität. Zur weiteren Regelung nutzen sie den Button 'Beleuchten' um den Lichteinfall zu ändern."
        self.text3=u"Unter dem Menüpunkt 'Ansicht' können sie folgendes einstellen:Fullscreen: Nächstes Molekül wird in einem gesonderten Fenster dargestellt, welches den kompletten Bildschirm ausfüllt. Zum Schließen ESC drücken.Bindegerüst: Beim nächsten Molekül werden die Bindungen so angepa"+u"sst, dass sich Kugeln und Zylinder nicht überschneiden, nützlich für transparente Darstellungen.Hintergrundfarbe: Hier können sie die Hintergrundfarbe des jeweiligen Moleküls ändern.Elementsymbole/Oxidationszahlen: Sie können sich die Oxidationszahl bzw. das Elementsymbol jedes Atoms anzeigen lassen."
        self.text4=u"Sie können unter dem Menüpunkt 'Datei' folgendes:PNG-Export: Speichern sie ein Bild des aktuell ausgewählten Moleküls im PNG-Format.SMILES-Import/Export: Mittels der SMILES-Notation zur vereinfachten Schreibweise von Molekülen können sie hier direkt eine 'Strukturformel' e"+u"ingeben und zeichnen lassen oder sich den SMILES-Code von einem mittels Analyse des Namens erstelltem Modell ausgeben lassen."
        self.text5=u"Unter dem Menüpunkt 'Datenbank erweitern' können sie mittels des erscheinenden Dialogfeldes:Präfixe/Suffixe funktionaler Gruppen dem Programm hinzufügenTrivialnamen ergänzen, die sie durch einen rationellen Namen umschreibenHinweis: Diese Datenbanken speichern im keinen Fa"+u"ll Strukturen von Molekülen, nur Bausteine aus denen dann ein Modell generiert wird bzw. Namen."
        self.text6=u"Unter dem Menüpunkt 'Atome' können sie die Einstellungen bzgl. der Atome ändern, also Farbe und Größe in der Darstellung verändern."
        self.text7=u"Sie haben zwei Möglichkeiten das Molekül zu drehen:1)Halten sie die rechte Maustaste gedrückt und bewegen die Maus, um das Molekül zu drehen.\n2)Die drei Schieberegler rechts neben demEingabefeld erlauben das Drehen um alle drei Achsen. Benutzen sie diese wenn sie z.B. e"+u"in Bild machen wollen, zum Betrachten eines Moleküls reicht meist die mausbasierte Steuerung."
    def OnLeftDClick(self, event):
        pt= event.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item:
            self.tree.SelectItem(item)
            i=self.tree.GetItemText(item)
            self.selecttext(i)
        event.Skip()
    def selecttext(self,name):
        self.textctrl.SetValue(eval("self.text"+str(self.namen.index(name)+1)))
def hilfefenster(parent):
    webbrowser.open("chython_hilfe/index.html")
    #hilfe=Hilfefenster(parent)
class vpythonscene(wx.Panel):
    def __init__(self,parent,scene):
        wx.Panel.__init__(self,parent,style=wx.BORDER_SUNKEN)
        self.scene=scene
        self.sza=None
    def setsza(self,a):
        self.sza=a
