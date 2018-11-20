#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, random, copy
from pygame.locals import *
from pygame.color import *

pygame.init()

escala = 20
ancho = 10
alto = 20

paleta = (
    (0, 0, 0),(255, 255, 255),(236, 14, 14), (238, 18, 18), (238, 90, 18), (238, 159, 12),
    (209, 238, 12), (127, 238, 12), (24, 238, 12), (12, 238, 99), (12, 238, 162), (12, 232, 238),
    (12, 140, 238), (12, 14, 238), (161, 12, 238), (238, 12, 100)
)
NEGRO = 0

piezas = (
    [[1,0],[0,1],[1,1]],#c
    [[1, 0],[-1,1],[0,1]],#s
    [[0,1],[1,1],[-1,0]],#z
    [[0,-1],[0,1],[1,1]],#l
    [[0,-1],[0,1],[-1,1]],#rl
    [[-1,0],[1,0],[0,1]],#t
    [[0,-1],[0,1],[0,2]]#p
)

def pinta(ventana, rect, color):
    rect.x += 20
    pygame.draw.rect(ventana, color, rect)

def color():
    return random.randint(1, len(paleta)-1)

def pinta_otros(ventana, pieza, puntos, level):
    margen = escala
    whidth = ancho*escala
    heigth = alto*escala
    c = paleta[1]
    font = pygame.font.SysFont("Latin", 30)
    fontN = pygame.font.SysFont("Latin", 60)

    sig = font.render("Siguiente", 1, c)
    pts = font.render("Puntos", 1, c)
    lv = font.render("Nivel", 1, c)
    escorre = fontN.render("{0:^5}".format(puntos), 1, c)
    dificultad = fontN.render("{0:^5}".format(level), 1, c)


    pygame.draw.line(ventana, THECOLORS["white"], (margen,0), (margen, heigth))
    pygame.draw.line(ventana, THECOLORS["white"], (margen,heigth), (whidth+margen, heigth))
    pygame.draw.line(ventana, THECOLORS["white"], (whidth+margen,heigth), (whidth+margen, 0))
    ventana.blit(sig, (whidth+(2*escala), 20))
    ventana.blit(pts, (whidth+(2*escala), 150))
    ventana.blit(lv, (whidth+(2*escala), 250))

    pieza.pinta(ventana)
    ventana.blit(escorre, (whidth+(2*escala), 180))
    ventana.blit(dificultad, (whidth+(2*escala), 280))


class tablero(object):
    def __init__(self):
        self.t = []

    def limpi(self):
        for i in range(alto):
            ta = []
            for j in range(ancho):
                ta.append(NEGRO)
            self.t.append(ta)

    def pinta(self, ventana):
        for i in range(alto):
            for j in range(ancho):
                rect = pygame.Rect((j*escala, i*escala), (escala-1, escala-1))
                pinta(ventana, rect, paleta[self.t[i][j]])

    def incrusta(self, pieza):
        for i in range(4):
            cor = pieza.cor(i)
            self.t[cor[1]][cor[0]] = pieza.color

    def colicion(self, pieza):
        for i in range(4):
            cor = pieza.cor(i)
            if self.t[cor[1]][cor[0]] != NEGRO:
                return True
        return False

    def __fila_llena(self, fila):
        for i in range(ancho):
            if self.t[fila][i] == NEGRO: return False
        return True

    def aplasta_filla(self, fila):
        for j in range(fila, 1, -1):
            for i in range(ancho):
                self.t[j][i] = self.t[j-1][i]

        for i in range(ancho):
            self.t[0][i] = NEGRO

    def colapsa(self):
        fila = alto-1
        multi = 0

        while fila > 0:
            if self.__fila_llena(fila):
                self.aplasta_filla(fila)
                multi += 1
            else: fila -= 1

        return (multi*3)*multi

    def limite(self):
        for i in range(ancho):
            if self.t[2][i] != NEGRO:
                return True
        return False

class pieza(object):
    def __init__(self):
        self.orig = [12, 4]
        self.perif = piezas[random.randint(0, len(piezas)-1)]
        self.color = color()
        self.espeed = escala
        self.incrusta = False

    def cor(self, pos):
        ret = (self.orig[0], self.orig[1])
        if pos != 0:
            ret = (ret[0]+self.perif[pos-1][0], ret[1]+self.perif[pos-1][1])
        return ret

    def pinta(self, ventana):
        for i in range(4):
            cor = self.cor(i)
            pinta(ventana, pygame.Rect((cor[0]*escala, cor[1]*escala), (escala-1, escala-1)), paleta[self.color])

    def __rota(self, cor):
        return [-cor[1], cor[0]]

    def rotar(self, t):
        p = []
        for i in range(len(self.perif)):
            p.append(self.perif[i])
            self.perif[i] = self.__rota(self.perif[i])

        for i in range(len(self.perif)):
            cor = self.cor(i+1)
            if cor[0] < 0 or cor[0] >= ancho:
                self.perif = p

        if t.colicion(self):
            self.perif = p

    def mueve(self, mov, t):
        x = self.orig[0]
        y = self.orig[1]

        self.orig[0] += mov[0]
        self.orig[1] += mov[1]

        for i in range(4):
            cor = self.cor(i)
            if cor[0] < 0 or cor[0] >= ancho:
                self.orig[0] = x
            if cor[1] < 0 or cor[1] >= alto:
                self.orig[1] = y
                self.incrusta = True

        if t.colicion(self):
            self.orig[0] = x
            self.orig[1] = y
            self.incrusta = True

    def coloca(self):
        self.orig = [4, 1]

    def handle(self, t, s):
        t.incrusta(self)
        return t.colapsa()



def main():
    ventana = pygame.display.set_mode((ancho*escala+150, alto*escala+escala))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    music = pygame.mixer.Sound("tetris.wav")

    p = pieza()
    s = pieza()
    t = tablero()
    tick = 0
    puntos = 0
    lv = 1
    espera = 60
    next = 30

    t.limpi()

    quit = False
    p.coloca()
    music.play(10)

    while not quit:
        for event in pygame.event.get():
            if event.type == QUIT: quit = True
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    p.rotar(t)
                if event.key == K_RIGHT:
                    p.mueve((1,0), t)
                    p.incrusta = False
                if event.key == K_LEFT:
                    p.mueve((-1,0), t)
                    p.incrusta = False
                if event.key == K_DOWN:
                    p.mueve((0,1), t)
                    if p.incrusta:
                        puntos += p.handle(t, s)
                        p = copy.deepcopy(s)
                        p.coloca()
                        s = pieza()


        if tick >= espera:
            tick = 0
            p.mueve((0,1), t)
            if p.incrusta:
                puntos += p.handle(t, s)
                p = copy.deepcopy(s)
                p.coloca()
                s = pieza()

        if puntos >= next:
            lv += 1
            espera -= 8
            next = next*2
            if escala < 5:
                espera = 5

        if t.limite():
            quit = True

        ventana.fill(paleta[NEGRO])
        t.pinta(ventana)
        p.pinta(ventana)
        pinta_otros(ventana, s, puntos, lv)
        pygame.display.update()
        clock.tick(60)
        tick += 1


    pygame.quit()

main()
