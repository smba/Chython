from Benutzeroberflaeche import beschreibung,ohnezahlen
def zerkleinere(a):
    #formt die Beschreibung so um, dass die zweiten elemente zu einer zahl werden
    #[ A, [ B, [0,2,0],[ C , [0,1,3.15]]]
    # -> [ A, [ B, 2, [ C, 1]]]
    #siehe auch zerkleinere_hoehere_ebene(
    a[0]=ohnezahlen(a[0])
    for i in range(len(a[1:])):
        a[i+1]=zerkleinere_hoehere_ebene(a[i+1])
    return a
def zerkleinere_hoehere_ebene(a):
    #wie zerkleinere fuer ebenen >1
    a[0]=ohnezahlen(a[0])
    for i in range(len(a[2:])):
        a[i+2]=zerkleinere_hoehere_ebene(a[i+2])
    a[1]=a[1][1]
    return a
def finde_laengstes(a):
    #loescht alle H
    a2=[a[0]]
    for i in a[1:]:
        if i[0]=="C":
            a2.append(finde_laengstes_hoehere_ebene(i))
    return a2
def finde_laengstes_hoehere_ebene(a):
    #wie finde_laengstes fuer ebenen >1
    a2=[a[0],a[1]]
    for i in a[2:]:
        if i[0]=="C":
            a2.append(finde_laengstes_hoehere_ebene(i))
    return a2
def spur(a):
    if len(a)==2 and type(a[1])==int:
        return 1
    ebenen=[]
    for i in a[1:]:
        if type(i)==int:
            #hoehere ebene
            continue
        ebenen.append(spur(i))
    return max(ebenen)+1
def finde_spur(a):
    for i in a[1:]:
        if type(i)==int:
            #hoehere ebene
            continue

print spur(finde_laengstes(zerkleinere(beschreibung("nonan"))))
