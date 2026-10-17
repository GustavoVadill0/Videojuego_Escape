# main.py
import pygame
import sys
from config import *
from mapa import GestorNivel
from entidades import Jugador, Monstruo
from motor_visual import MotorVisual

pygame.init()
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mansión V2 - Proyecto Modular")
reloj = pygame.time.Clock()

nivel = GestorNivel()
jugador = Jugador()
monstruo = Monstruo()
visuales = MotorVisual(WIDTH, HEIGHT)

estado = "JUGANDO" 
# main.py (Reemplaza la lógica de eventos y la de dibujo)

rectangulo_boton = pygame.Rect(BOTON_X, BOTON_Y, BOTON_ANCHO, BOTON_ALTO)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # --- NUEVO: DETECCIÓN DEL CLIC ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if estado in ["GAME OVER", "VICTORIA"]:
                if rectangulo_boton.collidepoint(event.pos):
                    nivel.reiniciar()
                    jugador.reiniciar()
                    monstruo.reiniciar()
                    estado = "JUGANDO"
                    
        # Movimiento del jugador
        if event.type == pygame.KEYDOWN and estado == "JUGANDO":
            movimiento = False
            if event.key == pygame.K_UP: movimiento = jugador.mover(0, -1, nivel)
            elif event.key == pygame.K_DOWN: movimiento = jugador.mover(0, 1, nivel)
            elif event.key == pygame.K_LEFT: movimiento = jugador.mover(-1, 0, nivel)
            elif event.key == pygame.K_RIGHT: movimiento = jugador.mover(1, 0, nivel)
                
            if movimiento and nivel.matriz[jugador.y][jugador.x] == 4:
                estado = "VICTORIA"
                
    # --- MOVIMIENTO INDEPENDIENTE DEL MONSTRUO ---
    if estado == "JUGANDO":
        # El monstruo se actualiza en cada fotograma, revisando su propio reloj
        monstruo.cazar(jugador.x, jugador.y, nivel)
        
        # Verificar colisión en tiempo real
        if jugador.x == monstruo.x and jugador.y == monstruo.y:
            estado = "GAME OVER"

    # --- FASE DE DIBUJO ---
    visuales.renderizar_mapa(pantalla, nivel.matriz)
    
    if estado == "JUGANDO":
        monstruo.dibujar(pantalla)
        jugador.dibujar(pantalla)
        visuales.dibujar_iluminacion(pantalla, jugador.x, jugador.y)
    
    elif estado in ["GAME OVER", "VICTORIA"]:
        # Dibujamos un velo negro semi-transparente sobre el mapa congelado
        pantalla.blit(visuales.capa_oscuridad, (0, 0)) 
        visuales.dibujar_interfaz_fin(pantalla, estado)

    pygame.display.flip()
    reloj.tick(FPS)