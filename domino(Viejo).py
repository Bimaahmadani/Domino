from pygame.locals import *
import random
import pygame
import sys


class Tablero:
    def __init__(self, PANTALLA):
        self.PANTALLA = PANTALLA
        self.fichas = []
        self.jugador_fichas = []
        self.computador_fichas = []
        self.fichas_jugadas = []
        self.Pos_fichas = []

    def creacion_fichas(self):
        for i in range(7):
            for j in range(i, 7):
                self.fichas.append([i,j])

        random.shuffle(self.fichas)

    def distribucion_dominos(self):
        for i in range(7):
            self.jugador_fichas.append(self.fichas[i])
            self.fichas.pop(i)

        for i in range(7):
            self.computador_fichas.append(self.fichas[i])
            self.fichas.pop(i)

        #print(len(self.jugador_fichas))
        #print(len(self.computador_fichas))
        #print(len(self.fichas))

    def revision_de_fichas(self, ficha):
        derecha = 0
        izquierda = 0
        derecha_girada = 0
        izquierda_girada = 0

        if len(self.fichas_jugadas) == 0 :
            return ficha, None

        if ficha.par[0] == self.fichas_jugadas[-1][0][1] :
            derecha = 1

        elif ficha.par[1] == self.fichas_jugadas[-1][0][1] :
            derecha = 1
            derecha_girada = 1

        if ficha.par[1] == self.fichas_jugadas[0][0][0] :
            izquierda = 1

        elif ficha.par[0] == self.fichas_jugadas[0][0][0] :
            izquierda = 1
            izquierda_girada = 1


        if (derecha == 1) and (izquierda == 1) :
            resultado = []

            if derecha_girada == 1 :
                resultado.extend([(ficha.par[1], ficha.par[0]), "derecha"])

            else :
                resultado.extend([ficha, "derecha"])

            if izquierda_girada == 1 :
                resultado.extend([(ficha.par[1], ficha.par[0]), "izquierda"])

            else :
                resultado.extend([ficha, "izquierda"])

            return resultado

        elif derecha == 1 :
            if derecha_girada == 1 :
                return (ficha.par[1], ficha.par[0]), "derecha"
            else :
                return ficha, "derecha"

        elif izquierda == 1 :
            if izquierda_girada == 1 :
                return (ficha.par[1], ficha.par[0]), "izquierda"
            else :
                return ficha, "izquierda"

        else :
            return None


    def dibujar_fichas(self, PANTALLA):
        espaciado = 18
        for i in range(len(self.jugador_fichas)):
            aux = Ficha(self.jugador_fichas[i][0], self.jugador_fichas[i][1], PANTALLA, espaciado, 335)
            self.Pos_fichas.append([espaciado, 335])
            self.jugador_fichas[i] = aux
            aux.mostrar_vertical()
            espaciado += 34

        for i in range(len(self.fichas)):
            aux = Ficha(self.fichas[i][0], self.fichas[i][1], PANTALLA, 260, 335)
            aux.mostrar_vertical()

        mascara = pygame.image.load(f"png/Fichas(Juego)/Parte_de_atras.png").convert()
        self.PANTALLA.blit(mascara, (260, 335))
        pygame.display.update()


class Ficha:
    def __init__(self, num1, num2, PANTALLA = None, X = 0, Y = 0):
        self.num1 = num1
        self.num2 = num2
        self.pos = [X, Y]
        self.par = [num1, num2]
        
        self.PANTALLA = PANTALLA
        self._X = X
        self._Y = Y      

        try:
            self.imagen = pygame.image.load(f"png/Fichas(Juego)/{num1}-{num2}.png").convert()
        except:
            self.imagen = pygame.image.load(f"png/Fichas(Juego)/{num2}-{num1}.png").convert()

    def mostrar_horizontal(self):
        x = self._X / 6
        angulo = 93-x
        	
        img = pygame.transform.rotate(self.imagen, angulo)
        img_rect = img.get_rect()

        self.PANTALLA.blit(img, img_rect)
        #pygame.display.flip()
        
        pygame.display.update()

    def mostrar_vertical(self):
        self.PANTALLA.blit(self.imagen, (self._X, self._Y))
        pygame.display.update()

    def cambiar_posicion(self, X, Y):
        self._X = X
        self._Y = Y

        self.PANTALLA.blit(self.imagen, (self._X, self._Y))
        pygame.display.update()
        

def click_ficha(posicion_mouse, posicion_ficha):
    if posicion_mouse[0] > posicion_ficha[0]\
    and posicion_mouse[0] < (posicion_ficha[0] + 34)\
    and posicion_mouse[1] > posicion_ficha[1]\
    and posicion_mouse[1] < (posicion_ficha[1] + 68) :
        return True
    else :
        return False


def jugada(tablero, ficha, resultado, PANTALLA):
    global NO_VA 
    NO_VA  = 0

    poner_ficha(ficha, tablero, PANTALLA, resultado[1])
    tablero.jugador_fichas.remove(ficha)

    if len(tablero.jugador_fichas) == 0:
        print("GANASTE!!")
    else:
        pass
        

def poner_ficha(ficha, tablero, PANTALLA, lugar = None):
    orientacion = "Vertical"
    reversaa = 0

    ficha_x = 0
    ficha_y = 0

    global primera_ficha_ABAJO
    global primera_ficha_IZQUIERDA
    global primera_ficha_ARRIBA
    global primera_ficha_DERECHA

    acotao = False
    if ficha.par[0] == ficha.par[1]:
        acotao = True

    if len(tablero.fichas_jugadas) == 0:
        if acotao:
            orientacion = "Vertical"
            tablero.fichas_jugadas.append(ficha)
            ficha.mostrar_vertical()
            ficha.cambiar_posicion(0, 0)


def run():
    pygame.init()
    PANTALLA = pygame.display.set_mode((700, 400))

    #Icono y Titulo
    icono = pygame.image.load("png/Domino(logo).png").convert()
    pygame.display.set_caption('Dominó!')
    pygame.display.set_icon(icono)

    #Fondo e Interfaz
    fondo = pygame.image.load("png/Domino.png").convert()
    PANTALLA.blit(fondo, (0, 0))

    #Tablero y Fichas
    tablero = Tablero(PANTALLA)
    tablero.creacion_fichas()
    tablero.distribucion_dominos()
    tablero.dibujar_fichas(PANTALLA)

    return tablero, PANTALLA
    

if __name__ == "__main__":
    tablero, PANTALLA = run()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                for ficha in tablero.jugador_fichas:
                    print(ficha)
                    if click_ficha(event.pos, ficha.pos):
                        resultado = tablero.revision_de_fichas(ficha.par)
                        #print(resultado)

                        if resultado is None:
                            pass

                        elif len(resultado) == 2:
                            jugada(tablero, ficha, resultado, PANTALLA)

                        #elif len(resultado) == 4:
                        #    izquierda_o_derecha(PANTALLA)
                            
                        

                    if click_ficha(event.pos, (260, 335)):
                        print("SIIIIII")

            pygame.display.update()

        pygame.display.update()