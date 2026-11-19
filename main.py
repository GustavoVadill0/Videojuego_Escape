
import pygame
import sys
from config import *
from mapa import Nivel, TOTAL_NIVELES
from entidades import Jugador, Monstruo
from motor_visual import MotorVisual
from sonidos import SistemaSonido


pygame.init()

pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape de la Mazmorra")
reloj = pygame.time.Clock()

# Inicializar el sistema de sonido 
sonidos = SistemaSonido()

nivel = Nivel(0)
jugador = Jugador()
monstruo = Monstruo()
visuales = MotorVisual(WIDTH, HEIGHT)

estado = "MENU_INICIO"
ultimo_estado_audio = estado
corriendo = True
aceleracion_activa = False

# Progreso de la partida
vidas = VIDAS_INICIALES
dificultad_actual = "normal"   # Se fija al elegirla en el menu y no cambia
tile_actual = TILE_SIZE        # Tamano de casilla del nivel actual
desplazamiento = (0, 0)        # Para centrar el mapa en la ventana

# Fuentes (se crean una sola vez)
fuente_titulo = pygame.font.SysFont(None, 58)
fuente_subtitulo = pygame.font.SysFont(None, 34)
fuente_boton = pygame.font.SysFont(None, 32)
fuente_poder = pygame.font.SysFont(None, 25)

# Botones de las pantallas finales
ancho_boton = 300
alto_boton = 48
espacio = 14
inicio_y = 160

# Dificultad base: (ms entre pasos del monstruo, radio de luz en casillas,
#                   oscuridad)
DIFICULTADES = {
    "facil": (600, 4, 250),
    "normal": (400, 3, 250),
    "dificil": (250, 2, 250),
}


def rects_botones(cantidad):
    return [
        pygame.Rect(
            WIDTH // 2 - ancho_boton // 2,
            inicio_y + i * (alto_boton + espacio),
            ancho_boton, alto_boton
        )
        for i in range(cantidad)
    ]


def opciones_finales():
    """Titulo, subtitulo, color y botones de cada pantalla final."""
    if estado == "GAME OVER":
        return (
            "¡TE ATRAPARON!", ROJO,
            f"Vidas restantes: {vidas}",
            [
                ("REINTENTAR NIVEL", "reintentar"),
                ("VOLVER AL MENU", "menu"),
                ("SALIR DEL JUEGO", "salir"),
            ]
        )

    if estado == "SIN VIDAS":
        return (
            "¡TE QUEDASTE SIN VIDAS!", ROJO,
            "Volveras al nivel 1",
            [
                ("VOLVER AL NIVEL 1", "reiniciar_juego"),
                ("VOLVER AL MENU", "menu"),
                ("SALIR DEL JUEGO", "salir"),
            ]
        )

    if estado == "VICTORIA":
        return (
            "¡ESCAPASTE!", VERDE,
            f"Nivel {nivel.numero} completado",
            [
                ("SIGUIENTE NIVEL", "siguiente"),
                ("VOLVER AL MENU", "menu"),
                ("SALIR DEL JUEGO", "salir"),
            ]
        )

    # JUEGO_COMPLETADO
    return (
        "¡JUEGO COMPLETADO!", VERDE,
        f"Escapaste de los {TOTAL_NIVELES} niveles",
        [
            ("VOLVER AL MENU", "menu"),
            ("SALIR DEL JUEGO", "salir"),
        ]
    )


def preparar_nivel():
    """Coloca al jugador y al monstruo y ajusta la dificultad del nivel."""
    global aceleracion_activa, tile_actual, desplazamiento

    datos = nivel.datos
    vel_base, luz_base, oscuridad = DIFICULTADES[dificultad_actual]

    # La dificultad elegida se combina con la del nivel
    monstruo.configurar_velocidad(
        int(vel_base * datos["factor_velocidad_monstruo"])
    )
    visuales.configurar_dificultad(
        luz_base * datos["factor_luz"], oscuridad
    )

    jx, jy = nivel.inicio_jugador
    mx, my = nivel.inicio_monstruo

    jugador.reiniciar(jx, jy)
    monstruo.reiniciar(mx, my)
    aceleracion_activa = False

    tile_actual, desplazamiento = visuales.calcular_vista(
        nivel.filas, nivel.columnas
    )


def iniciar_nivel(indice):
    nivel.cargar(indice)
    preparar_nivel()


def reintentar_nivel():
    nivel.reiniciar()
    preparar_nivel()


def nueva_partida():
    """Empieza desde el nivel 1 con todas las vidas."""
    global vidas

    vidas = VIDAS_INICIALES
    iniciar_nivel(0)


def comprobar_captura():
    global estado, vidas

    if monstruo.x == jugador.x and monstruo.y == jugador.y:
        if jugador.escudo_activo:
            jugador.escudo_activo = False
            monstruo.volver_al_inicio()
        else:
            vidas -= 1
            estado = "GAME OVER" if vidas > 0 else "SIN VIDAS"


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
                # La dificultad solo se elige aqui, antes de empezar la
                # partida. Una vez iniciada no se puede cambiar.
                elegida = None

                if visuales.rect_facil.collidepoint(pos_raton):
                    elegida = "facil"

                elif visuales.rect_normal.collidepoint(pos_raton):
                    elegida = "normal"

                elif visuales.rect_dificil.collidepoint(pos_raton):
                    elegida = "dificil"

                if elegida:
                    dificultad_actual = elegida
                    nueva_partida()
                    estado = "JUGANDO"

            elif estado in (
                "GAME OVER", "SIN VIDAS", "VICTORIA", "JUEGO_COMPLETADO"
            ):
                _, _, _, opciones = opciones_finales()
                rects = rects_botones(len(opciones))

                for (_, accion), rect in zip(opciones, rects):
                    if not rect.collidepoint(pos_raton):
                        continue

                    if accion == "reintentar":
                        reintentar_nivel()
                        estado = "JUGANDO"

                    elif accion == "siguiente":
                        iniciar_nivel(nivel.indice + 1)
                        estado = "JUGANDO"

                    elif accion == "reiniciar_juego":
                        nueva_partida()
                        estado = "JUGANDO"

                    elif accion == "menu":
                        nueva_partida()
                        estado = "MENU_INICIO"

                    elif accion == "salir":
                        corriendo = False

                    break

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
                if nivel.numero >= TOTAL_NIVELES:
                    estado = "JUEGO_COMPLETADO"
                else:
                    estado = "VICTORIA"

    # Controlar musica y sonidos cuando cambia el estado
    if estado != ultimo_estado_audio:

        if estado == "JUGANDO":
            sonidos.iniciar_musica()

        elif estado in ("GAME OVER", "SIN VIDAS"):
            sonidos.reproducir_derrota()

        elif estado in ("VICTORIA", "JUEGO_COMPLETADO"):
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
        visuales.renderizar_mapa(
            pantalla, nivel.matriz, tile_actual, desplazamiento
        )
        monstruo.dibujar(pantalla, tile_actual, desplazamiento)
        jugador.dibujar(pantalla, tile_actual, desplazamiento)

        visuales.dibujar_iluminacion(
            pantalla, jugador.x, jugador.y,
            tile_actual, desplazamiento
        )

        visuales.dibujar_hud(
            pantalla, nivel.llaves_recolectadas,
            vidas, VIDAS_INICIALES, nivel.numero, TOTAL_NIVELES
        )

        # Indicadores de los poderes activos
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

    elif estado in (
        "GAME OVER", "SIN VIDAS", "VICTORIA", "JUEGO_COMPLETADO"
    ):

        visuales.renderizar_mapa(
            pantalla, nivel.matriz, tile_actual, desplazamiento
        )
        pantalla.blit(visuales.capa_oscuridad, (0, 0))

        titulo, color_titulo, subtitulo, opciones = opciones_finales()

        texto = fuente_titulo.render(titulo, True, color_titulo)
        pantalla.blit(
            texto,
            (WIDTH // 2 - texto.get_width() // 2, 60)
        )

        texto_sub = fuente_subtitulo.render(subtitulo, True, BLANCO)
        pantalla.blit(
            texto_sub,
            (WIDTH // 2 - texto_sub.get_width() // 2, 110)
        )

        pos_raton = pygame.mouse.get_pos()

        for (texto_boton, _), rect in zip(
            opciones, rects_botones(len(opciones))
        ):
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
