import pygame
import random
import sys

pygame.init ()

#Constantes

ANCHO = 800
ALTO = 600
TAMANO_CELDA = 20
VELOCIDAD = 15

#Colores
NEGRO = (0,0,0)
VERDE = (0,255,0)
ROJO = (255,0,0)
BLANCO = (255,255,255)

#CONFIGURACION DE LA VENTANBA

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Snake')
reloj = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.posicion = [(ANCHO//2, ALTO//2)]
        self.direccion = [TAMANO_CELDA,0]
        self.crecer = False


    def mover(self):
        nueva_pos = (
        
            #(self.posicion[0][0] + self.direccion[0]) % ANCHO,
            #(self.posicion[0][1] + self.direccion[1]) % ALTO
        

            self.posicion[0][0] + self.direccion[0],
            self.posicion[0][1] + self.direccion[1]

        )

        if not (0 <= nueva_pos[0] < ANCHO and 0 <= nueva_pos[1] < ALTO):
            
            return False

        if not self.crecer:

            self.posicion.pop()

        else:

            self.crecer = False

        self.posicion.insert(0, nueva_pos)

        return True


    def cambiar_direccion(self, nueva_direccion):
        if (nueva_direccion[0] * -1, nueva_direccion[1] * -1) != self.direccion:
            self.direccion = nueva_direccion


    def comprobar_colision(self):
        return self.posicion[0] in self.posicion[1:]
    
class Comida:
    def __init__(self):
        self.posicion = self.generar_posicion()

    def generar_posicion(self):
        x = random.randrange (0, ANCHO, TAMANO_CELDA)
        y = random.randrange (0, ALTO, TAMANO_CELDA)
        return (x, y)
    
class Boton:
    
    def __init__(self, x, y, ancho, alto, texto):
        self.rect = pygame.Rect (x, y, ancho, alto)
        self.texto = texto
        self.color = (100, 100, 255)
        self.hover_color = (150, 150, 255)
        self.texto_color = NEGRO
        self.fuente = pygame.font.Font(None, 36)

    def dibujar(self, superficie):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect (superficie, color, self.rect)
        texto_surface = self.fuente.render (self.texto, True, self.texto_color)
        texto_rect = texto_surface.get_rect(center = self.rect.center)
        superficie.blit (texto_surface, texto_rect)

    def esta_clickeado(self, pos):
        return self.rect.collidepoint(pos)
    
def mostrar_game_over(superficie, puntuacion, boton_reiniciar):
    s = pygame.Surface((ANCHO, ALTO))
    s.set_alpha(128)
    s.fill(NEGRO)
    superficie.blit(s, (0, 0))

     #MENSAJE PERDISTE!
    fuente_grande = pygame.font.Font(None, 74)
    texto_perdiste = fuente_grande.render("PERDISTE!", True, ROJO)
    rect_perdiste = texto_perdiste.get_rect(center = (ANCHO//2, ALTO//2 - 50))
    superficie.blit (texto_perdiste, rect_perdiste)

     #PUNTUACION FINAL!
    fuente_normal = pygame.font.Font(None, 46)
    texto_puntuacion = fuente_normal.render(f"Puntuacion Final: {puntuacion}", True, BLANCO)
    rect_puntuacion = texto_puntuacion.get_rect(center = (ANCHO//2, ALTO//2 +20))
    superficie.blit(texto_puntuacion, rect_puntuacion)


    #Boton de Reinicio
    boton_reiniciar.dibujar(superficie)

def main():
    while True:
        jugar_partida()


def jugar_partida():
    snake = Snake()
    comida = Comida()
    puntuacion = 0
    game_over = False
    boton_reiniciar = Boton (ANCHO // 2 - 100, ALTO // 2 + 80, 200, 50, "Jugar de Nuevo")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and not game_over:
                if evento.key == pygame.K_UP:
                    snake.cambiar_direccion ((0, - TAMANO_CELDA))
                elif evento.key == pygame.K_DOWN:
                    snake.cambiar_direccion ((0, TAMANO_CELDA))
                elif evento.key == pygame.K_LEFT:
                    snake.cambiar_direccion ((- TAMANO_CELDA, 0))
                elif evento.key == pygame.K_RIGHT:
                    snake.cambiar_direccion ((TAMANO_CELDA, 0))
            elif evento.type == pygame.MOUSEBUTTONDOWN and game_over:
                if boton_reiniciar.esta_clickeado(evento.pos):
                    return #REINICIAR JUEGO
        
        if not game_over:
            if not snake.mover():

                game_over = True


        if snake.posicion[0] == comida.posicion:
            snake.crecer = True
            comida.posicion = comida.generar_posicion()
            puntuacion += 1

        if snake.comprobar_colision():
            game_over = True

        ventana.fill(NEGRO)


        for segmento in snake.posicion:
            #DIBUJAR LA SERPIENTE
            pygame.draw.rect(ventana, VERDE,
                             (segmento[0], segmento[1], TAMANO_CELDA - 1, TAMANO_CELDA - 1))

            #DIBUJAR COMIDA
            pygame.draw.rect(ventana, ROJO,
                            (comida.posicion[0], comida.posicion[1], TAMANO_CELDA-1, TAMANO_CELDA-1))
        

        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f'puntuacion: {puntuacion}', True, BLANCO)
        ventana.blit(texto, (10,10))

        if game_over:
            mostrar_game_over(ventana, puntuacion, boton_reiniciar)


        pygame.display.flip()
        reloj.tick(VELOCIDAD)

if __name__ =='__main__' :
    main()
