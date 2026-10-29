
import pygame
import sys
from config import *
from mapa import Nivel
from entidades import Jugador, Monstruo
from motor_visual import MotorVisual
from sonidos import SistemaSonido


pygame.init()

pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape de la Mazmorra")
reloj = pygame.time.Clock()

# Inicializar el sistema de sonido
sonidos = SistemaSonido()

nivel = Nivel()
jugador = Jugador()
monstruo = Monstruo()
visuales = MotorVisual(WIDTH, HEIGHT)

estado = "MENU_INICIO"
ultimo_estado_audio = estado
corriendo = True
aceleracion_activa = False


# Botones del menu final
ancho_boton = 300
alto_boton = 48
espacio = 14
inicio_y = 145

botones_finales = {
    "reintentar": pygame.Rect(
        WIDTH // 2 - ancho_boton // 2,
        inicio_y, ancho_boton, alto_boton
    ),
    "menu": pygame.Rect(
        WIDTH // 2 - ancho_boton // 2,
        inicio_y + alto_boton + espacio,
        ancho_boton, alto_boton
    ),
    "dificultad": pygame.Rect(
        WIDTH // 2 - ancho_boton // 2,
        inicio_y + 2 * (alto_boton + espacio),
        ancho_boton, alto_boton
    ),
    "salir": pygame.Rect(
        WIDTH // 2 - ancho_boton // 2,
        inicio_y + 3 * (alto_boton + espacio),
        ancho_boton, alto_boton
    )
}


def configurar_dificultad(opcion):
    if opcion == "facil":
        monstruo.configurar_velocidad(600)
        visuales.configurar_dificultad(TILE_SIZE * 4.5, 110)

    elif opcion == "normal":
        monstruo.configurar_velocidad(400)
        visuales.configurar_dificultad(TILE_SIZE * 3, 180)

    elif opcion == "dificil":
        monstruo.configurar_velocidad(250)
        visuales.configurar_dificultad(TILE_SIZE * 1.8, 250)


def reiniciar_partida():
    global aceleracion_activa

    nivel.reiniciar()
    jugador.reiniciar()
    monstruo.reiniciar()
    aceleracion_activa = False


def comprobar_captura():
    global estado

    if monstruo.x == jugador.x and monstruo.y == jugador.y:
        if jugador.escudo_activo:
            jugador.escudo_activo = False
            monstruo.x = 10
            monstruo.y = 5
            monstruo.ultimo_movimiento = pygame.time.get_ticks()
        else:
            estado = "GAME OVER"


def ejecutar_movimiento(dx, dy):
    # Guardar los poderes pendientes antes de moverse
    poderes_anteriores = len(nivel.poderes_pendientes)

    # El jugador identifica si recogio una llave
    resultado = jugador.mover(dx, dy, nivel)

    if resultado == "llave":
        sonidos.detener_movimiento()
        sonidos.reproducir_llave()

    elif resultado:
        if len(nivel.poderes_pendientes) > poderes_anteriores:
            sonidos.detener_movimiento()
            sonidos.reproducir_poder()
        else:
            sonidos.reproducir_movimiento()


def mover_jugador(dx, dy):
    global aceleracion_activa

    # Primer movimiento
    ejecutar_movimiento(dx, dy)
    comprobar_captura()

    if estado != "JUGANDO":
        return

    # Segundo movimiento cuando esta activa la aceleracion
    if aceleracion_activa:
        ejecutar_movimiento(dx, dy)
        comprobar_captura()


while corriendo:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            corriendo = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos_raton = event.pos

            if estado == "MENU_INICIO":
                if visuales.rect_jugar.collidepoint(pos_raton):
                    estado = "MENU_DIFICULTAD"

            elif estado == "MENU_DIFICULTAD":

                if visuales.rect_facil.collidepoint(pos_raton):
                    configurar_dificultad("facil")
                    reiniciar_partida()
                    estado = "JUGANDO"

                elif visuales.rect_normal.collidepoint(pos_raton):
                    configurar_dificultad("normal")
                    reiniciar_partida()
                    estado = "JUGANDO"

                elif visuales.rect_dificil.collidepoint(pos_raton):
                    configurar_dificultad("dificil")
                    reiniciar_partida()
                    estado = "JUGANDO"

            elif estado in ("GAME OVER", "VICTORIA"):

                if botones_finales["reintentar"].collidepoint(pos_raton):
                    reiniciar_partida()
                    estado = "JUGANDO"

                elif botones_finales["menu"].collidepoint(pos_raton):
                    reiniciar_partida()
                    estado = "MENU_INICIO"

                elif botones_finales["dificultad"].collidepoint(pos_raton):
                    reiniciar_partida()
                    estado = "MENU_DIFICULTAD"

                elif botones_finales["salir"].collidepoint(pos_raton):
                    corriendo = False

        elif event.type == pygame.KEYDOWN and estado == "JUGANDO":

            if event.key in (pygame.K_LEFT, pygame.K_a):
                mover_jugador(-1, 0)

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                mover_jugador(1, 0)

            elif event.key in (pygame.K_UP, pygame.K_w):
                mover_jugador(0, -1)

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                mover_jugador(0, 1)

    # Procesar poderes y perseguir al jugador
    if estado == "JUGANDO":

        ahora = pygame.time.get_ticks()

        for poder in nivel.poderes_pendientes:

            if poder == 6:
                monstruo.activar_ralentizacion()

            elif poder == 7:
                jugador.escudo_activo = True

            elif poder == 8:
                aceleracion_activa = True
                jugador.fin_aceleracion = ahora + 5000

        nivel.poderes_pendientes.clear()

        if (
            aceleracion_activa
            and ahora >= jugador.fin_aceleracion
        ):
            aceleracion_activa = False
            jugador.fin_aceleracion = 0

        monstruo.cazar(jugador.x, jugador.y, nivel)
        comprobar_captura()

        if estado == "JUGANDO":
            if nivel.matriz[jugador.y][jugador.x] == 4:
                estado = "VICTORIA"

    # Controlar musica y sonidos cuando cambia el estado
    if estado != ultimo_estado_audio:

        if estado == "JUGANDO":
            sonidos.iniciar_musica()

        elif estado == "GAME OVER":
            sonidos.reproducir_derrota()

        elif estado == "VICTORIA":
            sonidos.reproducir_victoria()

        else:
            sonidos.detener_musica()
            sonidos.detener_movimiento()

        ultimo_estado_audio = estado

    # Dibujar las pantallas
    if estado == "MENU_INICIO":
        visuales.dibujar_menu_inicio(pantalla)

    elif estado == "MENU_DIFICULTAD":
        visuales.dibujar_menu_dificultad(pantalla)

    elif estado == "JUGANDO":
        visuales.renderizar_mapa(pantalla, nivel.matriz)
        monstruo.dibujar(pantalla)
        jugador.dibujar(pantalla)

        visuales.dibujar_iluminacion(
            pantalla, jugador.x, jugador.y
        )

        visuales.dibujar_hud(
            pantalla, nivel.llaves_recolectadas
        )

        # Indicadores de los poderes activos
        fuente_poder = pygame.font.SysFont(None, 25)
        y_texto = 50

        if monstruo.fin_ralentizacion > pygame.time.get_ticks():
            texto = fuente_poder.render(
                "Monstruo ralentizado", True, (40, 180, 255)
            )
            pantalla.blit(texto, (10, y_texto))
            y_texto += 25

        if jugador.escudo_activo:
            texto = fuente_poder.render(
                "Escudo activo", True, (50, 220, 100)
            )
            pantalla.blit(texto, (10, y_texto))
            y_texto += 25

        if aceleracion_activa:
            texto = fuente_poder.render(
                "Aceleracion activa", True, (255, 220, 40)
            )
            pantalla.blit(texto, (10, y_texto))

    elif estado in ("GAME OVER", "VICTORIA"):

        visuales.renderizar_mapa(pantalla, nivel.matriz)
        pantalla.blit(visuales.capa_oscuridad, (0, 0))

        fuente_titulo = pygame.font.SysFont(None, 58)

        if estado == "GAME OVER":
            texto = fuente_titulo.render(
                "¡TE ATRAPARON!", True, ROJO
            )
        else:
            texto = fuente_titulo.render(
                "¡ESCAPASTE!", True, VERDE
            )

        pantalla.blit(
            texto,
            (WIDTH // 2 - texto.get_width() // 2, 65)
        )

        opciones = [
            ("REINTENTAR", "reintentar"),
            ("VOLVER AL MENU", "menu"),
            ("CAMBIAR DIFICULTAD", "dificultad"),
            ("SALIR DEL JUEGO", "salir")
        ]

        fuente_boton = pygame.font.SysFont(None, 32)
        pos_raton = pygame.mouse.get_pos()

        for texto_boton, accion in opciones:
            rect = botones_finales[accion]

            color = (
                (70, 130, 190)
                if rect.collidepoint(pos_raton)
                else GRIS_CLARO
            )

            pygame.draw.rect(
                pantalla, color, rect, border_radius=8
            )

            pygame.draw.rect(
                pantalla, BLANCO, rect, 2, border_radius=8
            )

            superficie_texto = fuente_boton.render(
                texto_boton, True, NEGRO
            )

            pantalla.blit(
                superficie_texto,
                (
                    rect.centerx - superficie_texto.get_width() // 2,
                    rect.centery - superficie_texto.get_height() // 2
                )
            )

    pygame.display.flip()
    reloj.tick(FPS)

# Detener el audio al cerrar el juego
sonidos.detener_movimiento()
sonidos.detener_musica()
pygame.quit()
sys.exit()
