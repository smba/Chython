# -*- coding: iso-8859-1 -*-
import wx
import wx.lib.agw.flatnotebook
from visual import *
from win32gui import *
from win32con import *
from random import randint
from copy import copy
from Benutzeroberflaeche import MyApp as MyAppForMolecules
global app
app=MyAppForMolecules()
def dreheab(a,n,winkel):
    for i in range(n+2,len(a),1):
        a[i]=rotate(a[i]-a[n],-winkel,a[n+1]-a[n])+a[n]
    return a
def drehvorschlaege1(a):
    global P1,P2,alt
    winkel=[]
    abstaende=[]
    for i in range(len(a)-2):
        if alt:
            s1 = proj(a[-1]-a[i],a[i+1]-a[i])
            s2 = proj(P1-a[i],a[i+1]-a[i])
            if mag(s1+a[i]-a[-1])<0.01 or mag(s2+a[i]-P1)<0.01:
                abstaende.append(mag(P1-a[i])*10+100000)
                if winkel==[]:
                    winkel=[0,i]
            else:
                winkel1=diff_angle(a[-1]-s1-a[i],P1-s2-a[i])
                _a=mag(rotate(a[-1]-a[i],winkel1,a[i+1]-a[i])+a[i]-P1)
                _b=mag(rotate(a[-1]-a[i],-winkel1,a[i+1]-a[i])+a[i]-P1)
                if _b>_a:
                    abstaende.append(_a)
                    winkel1=-winkel1
                else:
                    abstaende.append(_b)
                s1 = proj(a[-2]-a[i],a[i+1]-a[i])
                s2 = proj(P2-a[i],a[i+1]-a[i])
                abstaende[-1]*=mag(rotate(a[-2]-a[i],winkel1,a[i+1]-a[i])+a[i]-P2)
                if abstaende[-1]==min(abstaende) or winkel==[]:
                    winkel=[winkel1,i]
        else:
            s1 = proj(a[-2]-a[i],a[i+1]-a[i])
            s2 = proj(P2-a[i],a[i+1]-a[i])
            if mag(s1+a[i]-a[-2])<0.01 or mag(s2+a[i]-P2)<0.01:
                abstaende.append(mag(P2-a[-2])*10+100000)
                if winkel==[]:
                    winkel=[0,i]
            else:
                winkel1=diff_angle(a[-2]-s1-a[i],P2-s2-a[i])
                _a=mag(rotate(a[-2]-a[i],winkel1,a[i+1]-a[i])+a[i]-P2)
                _b=mag(rotate(a[-2]-a[i],-winkel1,a[i+1]-a[i])+a[i]-P2)
                if _b>_a:
                    abstaende.append(_a)
                    winkel1=-winkel1
                else:
                    abstaende.append(_b)
                s1 = proj(a[-1]-a[i],a[i+1]-a[i])
                s2 = proj(P1-a[i],a[i+1]-a[i])
                abstaende[-1]*=mag(rotate(a[-1]-a[i],winkel1,a[i+1]-a[i])+a[i]-P1)
                if abstaende[-1]==min(abstaende) or winkel==[]:
                    winkel=[winkel1,i]
    return abstaende,winkel
def drehezufaellig(a,winkel):
    for i in range(len(a)-2):
        a=dreheab(a,i,winkel.pop(0))
##def lastinvisible(self):
##    if self.naechstes:
##        if self.naechstes.naechstes:
##            self.naechstes.lastinvisible()
##        else:
##            self.kugel.visible=False
##            self.naechstes.kugel.visible=False
##            self.naechstes.bindung.visible=False
    return a
def kette(x,zl=0,zw=0,laengen=[],winkel=[]):
    l=10
    if laengen:
        l=laengen.pop(0)
   #nur zur Darstellung:
    a=[vector(0,10,0),vector(0,0,0)]
    for i in range(x-1):
        axis=a[-1]-a[-2]
        if zw:
            if randint(1,2)==1:
                axis=norm(rotate(axis,radians(randint(30,330)),vector(0,0,1)))
            else:
                axis=norm(rotate(axis,radians([60,180,300][randint(1,3)]),vector(0,0,1)))
        elif winkel:
            axis=norm(rotate(axis,pi-winkel.pop(0),vector(0,0,1)))
        else:
            axis=norm(rotate(axis,radians(180-109.48),vector(0,0,1)))
        if zl:
            axis*=randint(2,11)
        elif laengen:
            axis*=laengen.pop(0)
        else:
            axis*=10.
        a.append(a[-1]+axis)
    return a
def drehealledanach(a,b,n=0):
    for i in range(b):
        a=dreheab(a,n,2*pi/b)
        if a[n]!=a[-1]:
            a=drehealledanach(a,bn+1)
    return a
def drehealle(x,n,zl,zw):
    global curve1,facon,lmax
    a=kette(x,zl,zw)
    lmax=x*17
    if facon==2:
        curve1=curve(radius=0.1,color=(0.6,0.6,0.6),material=materials.plastic)
    elif facon==3:
        curve1=curve(visible=False)
##    a[-2]=vector(0,10,0)
##    a[-1]2=vector(0,0,0)

##    sphere(pos=a[-2],color=(1,1,0))
##    sphere(pos=a[-1]2,color=(1,0,1))
    a=drehealledanach(a,n)
    return a
def version1(a):
    global P1,P2,alt
    z=0
    alt=1
    while 1:
        z+=1
        abstaende,winkel = drehvorschlaege1(a)
        if (mag(a[-1]-P1)*mag(a[-2]-P2)-min(abstaende))<0.001:
            break
        a=dreheab(a,winkel[1],winkel[0])
        alt=not alt
    return  a,z,min(abstaende)
def annaeherung(x,zl,zw,laengen,winkel,gn=360,sim=False):
    global P1,P2
    P1=vector(0,0,0)
    P2=vector(0,10,0)
    n=0
    if not laengen:
        laengen=[10]+[10 for i in range(x-3)]+[10,10]
    if not winkel:
        winkel=[radians(109.48) for i in range(x-2)]+[pi/2]
    while n==0 or mag(a[-1]-P1)+mag(a[-2]-P2)>36./gn:
        n+=1
        a=kette(x,zl,zw,laengen,winkel)
        a=drehezufaellig(a,[randint(30,330) if randint(1,2)==2 else pi for i in range(x)])
        a,z,minabstaende=version1(a)
    if sim:
        for i in range(1,len(a)-1):
            sphere(pos=a[i],radius=1.5,material=materials.wood)
            cylinder(pos=a[i],axis=a[i+1]-a[i],radius=0.5,material=materials.wood)
    winkel=[0]
    for i in range(3,len(a)):
        winkel.append(diff_angle(a[i]-a[i-1]-proj(a[i]-a[i-1],a[i-1]-a[i-2]),a[i-3]-a[i-2]-proj(a[i-3]-a[i-2],a[i-1]-a[i-2])))
        if mag(rotate(a[i]-a[i-1]-proj(a[i]-a[i-1],a[i-1]-a[i-2]),winkel[-1],a[i-1]-a[i-2])-a[i-3]+a[i-2]+proj(a[i-3]-a[i-2],a[i-1]-a[i-2]))>0.01:
            winkel[-1]*=-1
    syntax=["C",[0,1,winkel[-2],0],["@1C",[0,1,winkel[-1]]],["H",[0,1,0]],["H",[0,1,0]]]
    winkel=winkel[:-2]
    winkel.reverse()
    for i in winkel:
        syntax=["C",[0,1,i,0],syntax,["H",[0,1,0]],["H",[0,1,0]]]
    syntax=["C",["@1C",[0,1,0]],syntax,["H",[0,1,0]],["H",[0,1,0]]]
    return syntax
class MyMenu(wx.Frame):
    def __init__(self,):
        wx.Frame.__init__(self, None,-1,"Drehsimulation",(0,0), wx.Size(1366, 738))
        #Fenster wird aufgeteilt, um spaeter ein VPythonfenster einbauen zu koennen
        self.Show(False)
        self.Splitter=wx.SplitterWindow(self,style=wx.SP_3DBORDER|wx.SP_3DSASH)
        self.panel=wx.Panel(self.Splitter,style=wx.BORDER_SUNKEN)
        self.vpythonnotebook=wx.lib.agw.flatnotebook.FlatNotebook(self.Splitter,style=wx.NB_MULTILINE)
        self.Splitter.SplitHorizontally(self.vpythonnotebook,self.panel,590)
        self.vpython1=wx.Panel(self.vpythonnotebook,style=wx.BORDER_SUNKEN)
        self.vpythonnotebook.AddPage(self.vpython1,"")
##        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.notebookpagechanged,self.vpythonnotebook)
        self.vpython1.SetBackgroundColour("black")
        self.scene=display(ambient=0.5,background=(0.3,0.3,0.3),autocenter=True)
        font1 = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font2 = wx.Font(11, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)
        self.hoelzer=wx.Slider(self.panel,1,4,0,100,pos=(10,40),size=(200,-1),style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        t1=wx.StaticText(self.panel,-1,"Anzahl Ebenen",pos=(10,10))
        t1.SetFont(font1)
        t2=wx.StaticText(self.panel,-1,u"Art der Endverknüpfung",pos=(250,10))
        t2.SetFont(font1)
        self.r1=wx.RadioBox(self.panel, -1, "", (250,35),(t2.GetSize()[0],-1),["Keine     ","Kugeln     ","Graph     ","faces     "], 2, wx.RA_SPECIFY_COLS)
        self.r1.SetFont(font2)
        t3=wx.StaticText(self.panel,-1,u"Form der Bewegung",pos=(t2.GetSize()[0]+t2.GetPosition()[0]+15,10))
        t3.SetFont(font1)
        self.r2=wx.RadioBox(self.panel, -1, "", (t3.GetPosition()[0],35),(t3.GetSize()[0],-1),["Alles drehen","Lokale Suche"], 1, wx.RA_SPECIFY_COLS)
        self.r2.SetFont(font2)
        t4=wx.StaticText(self.panel,-1,u"Ketteneigenschaften",pos=(t3.GetSize()[0]+t3.GetPosition()[0]+15,10))
        t4.SetFont(font1)
        self.cb3=wx.CheckBox(self.panel, -1,u"zufällige Längen",(t4.GetPosition()[0]+5,48),(170,20))
        self.cb4=wx.CheckBox(self.panel, -1,u"zufällige Winkel",(t4.GetPosition()[0]+5,67),(170,20))
        wx.StaticBox(self.panel,-1,"",(t4.GetPosition()[0],37),(t4.GetSize()[0],self.r2.GetSize()[1]-2))
        self.cb3.SetFont(font2)
        self.cb4.SetFont(font2)
        t1=wx.StaticText(self.panel,-1,"Genauigkeit",pos=(t4.GetSize()[0]+t4.GetPosition()[0]+15,10))
        t1.SetFont(font1)
        self.genauigkeit=wx.Slider(self.panel,1,10,1,360,pos=(t1.GetPosition()[0],35),size=(200,-1),style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)
        self.genauigkeit.SetTickFreq(0)
        b1=wx.Button(self.panel,-1,"Simulation",pos=(t1.GetPosition()[0]+215,10),size=(100,30))
        b1.SetFont(font1)
        self.panel.Bind(wx.EVT_BUTTON,self.simulation,b1)
    def setwindow(self):
        h=sphere()
        VP = FindWindow ( None, "Simulation")
        flags = SWP_SHOWWINDOW or \
            SWP_FRAMECHANGED
        SetWindowPos(VP, HWND_TOPMOST,-5,-32,1360,600, flags)
        SetParent (VP,self.vpython1.GetHandle ())
        h.visible=False
    def simulation(self,evt):
        global facon,curve1,lmax,app
        facon=self.r1.GetSelection()
        if self.r2.GetSelection()==0:
            self.display=display(ambient=1,title="Simulation",background=(0,0,0))
            local_light(pos=(0,-10,0))
            self.setwindow()
            drehealle(self.hoelzer.GetValue(),self.genauigkeit.GetValue(),self.cb3.GetValue(),self.cb4.GetValue())
            #face
            if self.r1.GetSelection()==3:
                g=self.genauigkeit.GetValue()
                cp=len(curve1.pos)
                f1=faces(material=materials.wood)
                f1.pos=[vector(0,0,0) for i in range(len(curve1.pos)*3)]
                #f1.normal=zeros((cp*3,3),int)
                for n in range(cp):
                    f1.pos[n*3-1]=curve1.pos[n-2]
                    f1.pos[n*3-2]=curve1.pos[n-1]
                    f1.pos[n*3-3]=curve1.pos[n-g]
                    f1.normal[n]=vector(100,0,0)
                    f1.normal[n+2*cp]=vector(100,0,0)
                    f1.color[n]=(mag(curve1.pos[n-1]+curve1.pos[n-2]+curve1.pos[n-g])/3*1./lmax,0,1-mag(curve1.pos[n-1]+curve1.pos[n-2]+curve1.pos[n-g])/3*1./lmax)
                    f1.color[n+cp]=(mag(curve1.pos[n-1]+curve1.pos[n-2]+curve1.pos[n-g])/3*1./lmax,0,1-mag(curve1.pos[n-1]+curve1.pos[n-2]+curve1.pos[n-g])/3*1./lmax)
                    f1.color[n+2*cp]=(mag(curve1.pos[n-1]+curve1.pos[n-2]+curve1.pos[n-g])/3*1./lmax,0,1-mag(curve1.pos[n-1]+curve1.pos[n-2]+curve1.pos[n-g])/3*1./lmax)
                f1.pos=zeros((cp*3,3),int)+f1.pos
                f1.normal=zeros((cp*3,3),int)+f1.normal
                for n in range(cp):
                    f1.pos[n*3-1]=curve1.pos[n-1]
                    f1.pos[n*3-2]=curve1.pos[n-2]
                    f1.pos[n*3-3]=curve1.pos[n-g]
                    f1.normal[n+cp]=vector(100,0,0)
                f1.smooth()
        else:
            self.display=display(ambient=1,title="Simulation",background=(0.3,0.3,0.3),visible=False)
            self.display.select()
            local_light(pos=(0,-10,0))
            syntax=annaeherung(self.hoelzer.GetValue(),self.cb3.GetValue(),self.cb4.GetValue(),[],[],self.genauigkeit.GetValue(),True)
            try:
                app.zeichne(syntax)
            except wx._core.PyDeadObjectError:
                app=MyAppForMolecules(0)
                app.zeichne(syntax)
            self.display.visible=True
            self.setwindow()
            ##print "letzte Annäherung   :",mag(a[-1]-P1)+mag(a[-2]-P2)-minabstaende
            ##print "finaler Abstand 1   :",mag(a[-1]-P1)
            ##print "finaler Abstand 2   :",mag(a[-2]-P2)
            print "------------------------------"
            print
            self.display.autocenter=True
class MyApp(wx.App):
    def OnInit(self):
        frame=MyMenu()
        frame=frame.Show(True)
        return True
# *~*~*~*~*~*~*~*~*~*~*~*~*
#bis hierhin ausfuehren
# *~*~*~*~*~*~*~*~*~*~*~*~*
a=MyApp(0)
a.MainLoop()
