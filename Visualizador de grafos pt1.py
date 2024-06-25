"Carlos Murillo Aguilar"
import random
import math
import sys
import pygame
from pygame.locals import *
pygame.init()

def spring(nodos,aristas,Gnodos):   # Función para la generación visual del grafo
    a=30                            #  mediante el método de resorte
    c1=10 # Variables para estabilizar visualización
    c2=19
    c3=0.18
    c4=.1
    fuerzas=[]
    for r in range(len(nodos)):
        a=True
        while a==True:
            x=random.randrange(375,625,5) # Asignación de coordenadas al azar
            y=random.randrange(175,425,5)
            if [x,y] not in Gnodos:
                Gnodos.append([x,y])
                a=False
    screen = pygame.display.set_mode((1000,600)) # Inicio de la pantalla de visualización
    
    # for rep in range(100):
    # print(Gnodos)
    # clock = pygame.time.Clock()
    while True:
        # clock.tick(1)
        for event in pygame.event.get(): # Función para poder cerrar la pantalla
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.fill('white')
        for n in Gnodos:
            pygame.draw.circle(screen, 'black', (n[0], n[1]), 9) # Dibujo de cada nodo
        for e in aristas:
            e0=e[0]
            e1=e[1]
            e0ind=nodos.index(e0)
            # print(e0ind)
            e1ind=nodos.index(e1)
            # print(e1ind)
            # print("LX0= ",Gnodos[e0ind][0])
            Lx0=Gnodos[e0ind][0]
            # print("LX1= ",Gnodos[e0ind][1])
            Ly0=Gnodos[e0ind][1]
            # print("LY0= ",Gnodos[e1ind][0])
            Lx1=Gnodos[e1ind][0]
            # print("LY1= ",Gnodos[e1ind][1])
            Ly1=Gnodos[e1ind][1]
            pygame.draw.line(screen, 'black', (Lx0,Ly0), (Lx1,Ly1))
        
        for j in range(len(nodos)):
            fx=0
            fy=0
            for k in range(len(nodos)):
                fxn=0
                fyn=0
                dx=0
                dy=0
                d=0
                alpha=0
                fn=0
                if nodos[j] != nodos[k]:        #Cálculo de las distancias entre cada nodo
                    dx=Gnodos[k][0]-Gnodos[j][0]
                    dy=Gnodos[k][1]-Gnodos[j][1]
                    d=math.sqrt((dx)**2 + (dy)**2)
                    alpha=math.asin(dy/d)
                    if [nodos[j],nodos[k]] in aristas:
                        fn=c1*math.log((d/c2),10)   # Cálculo de la fuerza de atracción
                        if dx>0:                    # entre nodos unidos por arista
                            if d<c2:
                                fxn=-a*abs(fn*math.cos(alpha))
                            else:
                                fxn=abs(fn*math.cos(alpha))
                        elif dx<0:
                            if d<c2:
                                fxn=a*abs(fn*math.cos(alpha))
                            else:
                                fxn=-abs(fn*math.cos(alpha))
                        if dy>0:
                            if d<c2:
                                fyn=-a*abs(fn*math.sin(alpha))
                            else:
                                fyn=abs(fn*math.sin(alpha))
                        elif dy<0:
                            if d<c2:
                                fyn=a*abs(fn*math.sin(alpha))
                            else:
                                fyn=-abs(fn*math.sin(alpha))
                    else:
                        fn=c3/math.sqrt(0.5*d)      #Cálculo de la fuerza de repulsión
                        if dx>0:
                            fxn=-abs(fn*math.cos(alpha))
                        elif dx<0:
                            fxn=abs(fn*math.cos(alpha))
                        if dy>0:
                            fyn=-abs(fn*math.sin(alpha))
                        elif dy<0:
                            fyn=abs(fn*math.sin(alpha))
                    fx += fxn
                    fy += fyn
            fuerzas.append([fx,fy])
        cx=0
        cy=0
        for j in range(len(Gnodos)):                    # Asignación de las nuevas coordenadas
            if Gnodos[j][1]>10 and Gnodos[j][1]<590:    # en función de la suma de fuerzas en cada nodo
                cy=Gnodos[j].pop(1)+c4*fuerzas[j][1]
            else:
                cy=Gnodos[j].pop(1) -80*c4*fuerzas[j][1]
                
            if Gnodos[j][0]>10 and Gnodos[j][0]<990:
                cx=Gnodos[j].pop(0)+c4*fuerzas[j][0]
            else:
                cx=Gnodos[j].pop(0) -80*c4*fuerzas[j][0]
            Gnodos[j].insert(0,cx)
            Gnodos[j].insert(1,cy)
        pygame.display.update()     # Acutualización de pantalla
        fuerzas.clear()

"Visualizar grafo"          # Función para leer un archivo gv con el nombre grafo
def visual(tipo):
    s=open("grafo.gv","r")
    linea_Lectura=[]
    arista_Lectura=[]
    aristas=[]
    nodos=[]
    rL=s.readlines()
    for i in range(1, len(rL)-1):
        if "->" in rL[i]:
            linea_Lectura.append(rL[i][0:-2])        
            arista_Lectura.append(linea_Lectura[i-1].split(" -> "))
            e0=int(arista_Lectura[i-1][0])
            e1=int(arista_Lectura[i-1][1])
            arista_Lectura[i-1][0]=e0
            arista_Lectura[i-1][1]=e1
            if e0 not in nodos:
                nodos.append(e0)
            if e1 not in nodos:
                nodos.append(e1)
            if [e0,e1] not in aristas and [e1,e0] not in aristas:
                aristas.append([e0,e1])
        else:
            linea_Lectura.append(rL[i][0:-2])
            arista_Lectura.append(linea_Lectura[i-1])
            e0=int(aristas[i-1])
            nodos.append(e0)
    nodos.sort()
    print(nodos)
    # print(aristas)
    if tipo==Spring:
        Gnodos=[]
        spring(nodos,aristas,Gnodos)

Spring="Spring"
visual(Spring)