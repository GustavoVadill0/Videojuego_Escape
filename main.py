import pygame
import sys
from config import *
from mapa import Nivel
from entidades import Jugador, Monstruo
from motor_visual import MotorVisual

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape de la Mazmorra")
reloj = pygame.time.Clock()

# Instanciar objetos
nivel = Nivel()
jugador = Jugador()
monstruo = Monstruo()
visuales = MotorVisual(WIDTH, HEIGHT)

estado = "MENU_INICIO" # Estados posibles: "MENU_INICIO", "JUGANDO", "GAME OVER", "VICTORIA"

corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_raton = pygame.mouse.get_pos()

            if estado == "MENU_INICIO":
                if visuales.rect_facil.collidepoint(pos_raton):
                    monstruo.configurar_velocidad(600)
                    visuales.configurar_dificultad(TILE_SIZE * 4.5)
                    estado = "JUGANDO"
                elif visuales.rect_normal.collidepoint(pos_raton):
                    monstruo.configurar_velocidad(400)
                    visuales.configurar_dificultad(TILE_SIZE * 3)
                    estado = "JUGANDO"
                elif visuales.rect_dificil.collidepoint(pos_raton):
                    monstruo.configurar_velocidad(250)
                    visuales.configurar_dificultad(TILE_SIZE * 1.8)
                    estado = "JUGANDO"

            elif estado in ["GAME OVER", "VICTORIA"]:
                rect_boton = pygame.Rect(BOTON_X, BOTON_Y, BOTON_ANCHO, BOTON_ALTO)
                if rect_boton.collidepoint(pos_raton):
                    estado = "MENU_INICIO"
                    nivel.reiniciar()
                    jugador.reiniciar()
                    monstruo.reiniciar()

        elif event.type == pygame.KEYDOWN and estado == "JUGANDO":
            if event.key in (pygame.K_LEFT, pygame.K_a):
                jugador.mover(-1, 0, nivel)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                jugador.mover(1, 0, nivel)
            elif event.key in (pygame.K_UP, pygame.K_w):
                jugador.mover(0, -1, nivel)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                jugador.mover(0, 1, nivel)

    # Lógica del juego
    if estado == "JUGANDO":
        monstruo.cazar(jugador.x, jugador.y, nivel)

        # Condición de derrota
        if monstruo.x == jugador.x and monstruo.y == jugador.y:
            estado = "GAME OVER"

        # Condición de victoria
        if nivel.matriz[jugador.y][jugador.x] == 4:
            estado = "VICTORIA"

    # Fase de dibujo
    if estado == "MENU_INICIO":
        visuales.dibujar_menu_inicio(pantalla)

    elif estado == "JUGANDO":
        visuales.renderizar_mapa(pantalla, nivel.matriz)
        monstruo.dibujar(pantalla)
        jugador.dibujar(pantalla)
        visuales.dibujar_iluminacion(pantalla, jugador.x, jugador.y)
        visuales.dibujar_hud(pantalla, nivel.llaves_recolectadas)

    elif estado in ["GAME OVER", "VICTORIA"]:
        visuales.renderizar_mapa(pantalla, nivel.matriz)
        pantalla.blit(visuales.capa_oscuridad, (0, 0))
        visuales.dibujar_interfaz_fin(pantalla, estado)

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
sys.exit()