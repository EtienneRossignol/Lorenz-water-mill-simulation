from tkinter import *
from math import pi,sin,cos
from PIL import Image

NB_CONE=12
H=80
RAYON=50
DEBIT=14500
FACTEUR_mHL=(H**2)/(RAYON**2)/3
RAYON_CENTRAL=300
T=800
TROU=12
DELTA=.1
FROTTEMENT=.98
VITESSE=.4
vitesse_max=0.08
masse_max=FACTEUR_mHL*(H**3)*NB_CONE

x_avant,y_avant=-1,-1
acc_avant, masse_avant=-1,-1
fen =Tk()
fen.geometry(str(T*2)+'x'+str(T)+'+50+5')
fen.title('Moulin à eau de Lorenz     --- Etienne ROSIGNOL --- ')
C=Canvas(fen,width=T,height=T)
C.pack(side=LEFT)
graphe=Canvas(fen,width=T,height=T)
graphe.pack(side=LEFT)

im=Image.open("degrade.png")
size = im.size
pix=im.load()
graphe.create_line(0,T/4*3,T/2,T/4*3)
graphe.create_line(T/4,0,T/4,T)
graphe.create_line(0,T/4,T,T/4)
graphe.create_line(T/4*3,0,T/4*3,T/2)

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

    @staticmethod
    def couleur(nb,nb_max ):
        pos=nb+nb_max/2
        pos*=size[0]/nb_max

        r,g,b,alpha=pix[round(pos),size[1]//2]
        return '#'+hex(r)[2:].rjust(2,'0')+hex(g)[2:].rjust(2,'0')+hex(b)[2:].rjust(2,'0')

    @classmethod
    def masse_t(self):
        masse=0
        for obj in self.L:
            masse+=obj.masse
        return masse

def ligne(x1,y1,x2,y2,x_pos,y_pos):
    x1,y1,x2,y2=map(lambda x:(x*RAYON_CENTRAL +RAYON_CENTRAL)/RAYON_CENTRAL*T/4,(x1,y1,x2,y2))
    x1,x2=x1+x_pos*T/2,x2+x_pos*T/2
    y1,y2=y1+y_pos*T/2,y2+y_pos*T/2

    return x1,y1,x2,y2

for i in range(NB_CONE):cone(i)
def tour():
    global x_avant,y_avant,acc_avant, masse_avant
    C.delete(ALL)
    cone.update()
    C.create_line(T/2,0,T/2,100,fill='red',smooth=True,width=5)

    x,y=cone.L[0].centre_gravite
    acc,masse= cone.acceleration(),cone.masse_t()

    C.create_oval(x*RAYON_CENTRAL+T/2-5,y*RAYON_CENTRAL+T/2-5,
                  x*RAYON_CENTRAL+T/2+5,y*RAYON_CENTRAL+T/2+5,width=0,
                  fill=cone.couleur(cone.vitesse, vitesse_max))
    C.create_line(T//2,y*RAYON_CENTRAL+T/2-25,T//2,y*RAYON_CENTRAL+T/2+25)
    if (x_avant,y_avant)!=(-1,-1):
        x1,y1,x2,y2=ligne(x_avant,y_avant,x,y,0,0)
        graphe.create_line(x1,y1,x2,y2,fill=cone.couleur(cone.vitesse, vitesse_max))

        x1,y1,x2,y2=ligne(x_avant,y_avant,x,y,1,0)
        graphe.create_line(x1,y1,x2,y2,fill=cone.couleur((cone.masse_t()-masse_max/4)*2, masse_max))

        x1,y1,x2,y2=ligne(acc_avant*RAYON_CENTRAL, (masse_avant-masse_max/2)/masse_max*2,
                          acc*RAYON_CENTRAL,(masse_avant-masse_max/2)/masse_max*2,0,1)
        graphe.create_line(x1,y1,x2,y2,fill=cone.couleur(cone.vitesse, vitesse_max))

    acc_avant, masse_avant=acc,masse
    x_avant,y_avant=x,y

    fen.after(40, tour)
tour()

fen.resizable(width=False,height=False)
fen.mainloop()