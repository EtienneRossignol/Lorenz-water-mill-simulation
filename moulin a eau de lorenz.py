from tkinter import *
from math import pi,sin,cos
from PIL import Image

NB_CONE=12
H=80
RAYON=50
DEBIT=15000
FACTEUR_mHL=(H**2)/(RAYON**2)/3
RAYON_CENTRAL=300
T=800
TROU=12
DELTA=.1
FROTTEMENT=.98
VITESSE=.4
vitesse_max=0.4

x_avant,y_avant=-1,-1
fen =Tk()
C=Canvas(fen,width=T,height=T)
C.pack(side=LEFT)
graphe=Canvas(fen,width=T,height=T)
graphe.pack(side=LEFT)

im=Image.open("degrade.png")
size = im.size
pix=im.load()

class cone:
    vitesse=0
    delta=DELTA
    L=[]
    def __init__(self, position):
        self.rayon=RAYON
        self.hauteur=H
        self.masse=0
        self.position=position/NB_CONE*2*pi
        cone.L.append(self)

    @property
    def h(self):
        return (self.masse/FACTEUR_mHL)**(1/3)
        
    def updat(self):
        if abs(cos(cone.delta+self.position))*RAYON_CENTRAL<self.rayon and \
            sin(cone.delta+self.position)*RAYON_CENTRAL<.1 :
            self.masse+=DEBIT
            

        self.masse-=self.h*TROU
        if self.masse<0:
            self.masse=0
        elif self.h>self.hauteur :
            self.masse=FACTEUR_mHL*(self.hauteur**3)
            #print(self.h,self.masse)

    @classmethod
    def acceleration(class1):
        nominateur=0
        denominateur=0

        for obj in class1.L:
            nominateur+=obj.masse*cos(class1.delta+obj.position)
            denominateur+=obj.masse*RAYON_CENTRAL#**2

        if denominateur:
            return nominateur/denominateur
        return 0

    def affich(self):
        x_centre=cos(cone.delta+self.position)*RAYON_CENTRAL+T/2
        y_haut=sin(cone.delta+self.position)*RAYON_CENTRAL+T/2
        
        C.create_polygon(x_centre,y_haut+self.hauteur,
                         x_centre-self.rayon*(self.h/self.hauteur),y_haut+self.hauteur-self.h,
                         x_centre+self.rayon*(self.h/self.hauteur),y_haut+self.hauteur-self.h,
                         fill='blue')

        C.create_line(x_centre-self.rayon,y_haut,x_centre,y_haut+self.hauteur)
        C.create_line(x_centre+self.rayon,y_haut,x_centre,y_haut+self.hauteur)

    @property
    def centre_gravite(self):
        masse=0
        X=0
        Y=0
        for obj in self.L:
            x=cos(self.delta+obj.position)
            y_bas=sin(self.delta+obj.position)+obj.hauteur/RAYON_CENTRAL
            y=y_bas-obj.h*4/5/RAYON_CENTRAL
            X+=x*obj.masse
            Y+=y*obj.masse
            masse+=obj.masse
        return X/masse, Y/masse
            
    @staticmethod
    def update():
        cone.vitesse+=cone.acceleration()*VITESSE
        cone.vitesse*=FROTTEMENT
        cone.delta+=cone.vitesse
        for obj in cone.L:
            obj.updat()
            obj.affich()

    @classmethod
    def couleur(class1):
        pos=class1.vitesse+vitesse_max/2
        pos*=size[0]/vitesse_max
        
        r,g,b=pix[round(pos),size[1]//2]
        return '#'+hex(r)+hex(g)+hex(b)

for i in range(NB_CONE):cone(i)

def tour():
    global x_avant,y_avant
    C.delete(ALL)
    cone.update()
    C.create_line(T/2,0,T/2,100,fill='blue',smooth=True,width=5)

    x,y=cone.L[0].centre_gravite

    C.create_oval(x*RAYON_CENTRAL+T/2-5,y*RAYON_CENTRAL+T/2-5,
                  x*RAYON_CENTRAL+T/2+5,y*RAYON_CENTRAL+T/2+5,width=0,fill=cone.couleur())
    C.create_line(T//2,y*RAYON_CENTRAL+T/2-25,T//2,y*RAYON_CENTRAL+T/2+25)
    if (x_avant,y_avant)!=(-1,-1):
        graphe.create_line(x_avant*RAYON_CENTRAL+T/2,y_avant*RAYON_CENTRAL+T/2,
                           x*RAYON_CENTRAL+T/2,y*RAYON_CENTRAL+T/2)
    x_avant,y_avant=x,y
    fen.after(50, tour)
tour()

fen.resizable(width=False,height=False)
fen.mainloop()
