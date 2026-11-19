
import pygame
from config import *


class MotorVisual:

    def __init__(self, ancho, alto):
        self.capa_oscuridad = pygame.Surface(
            (ancho, alto), pygame.SRCALPHA
        )

        # El radio de luz se expresa en CASILLAS (asi se adapta al tamano
        # de casilla de cada nivel)
        self.radio_luz = 3
        self.alfa_oscuridad = 180

        def cargar_img(ruta):
            return pygame.image.load(ruta).convert_alpha()

        self._img_muro = cargar_img("assets/muro.png")
        self._img_puerta = cargar_img("assets/puerta.png")
        self._img_llave = cargar_img("assets/llave.png")
        self._img_salida = cargar_img("assets/salida.png")
        self._cache_tiles = {}

        self.fuente_hud = pygame.font.SysFont(None, 32)
        self.img_llave_hud = pygame.transform.scale(
            self._img_llave, (25, 25)
        )

        self.rect_jugar = pygame.Rect(
            WIDTH // 2 - 110, HEIGHT // 2, 220, 55
        )

        self.rect_facil = pygame.Rect(
            WIDTH // 2 - 110, 190, 220, 50
        )

        self.rect_normal = pygame.Rect(
            WIDTH // 2 - 110, 260, 220, 50
        )

        self.rect_dificil = pygame.Rect(
            WIDTH // 2 - 110, 330, 220, 50
        )

    def calcular_vista(self, filas, columnas):
        """Tamano de casilla y desplazamiento para centrar el mapa."""
        tile = min(TILE_MAX, WIDTH // columnas, HEIGHT // filas)

        ox = (WIDTH - columnas * tile) // 2
        oy = (HEIGHT - filas * tile) // 2

        return tile, (ox, oy)

    def _imagenes(self, tile):
        if tile not in self._cache_tiles:
            def esc(img):
                return pygame.transform.scale(img, (tile, tile))

            muro = esc(self._img_muro)

            self._cache_tiles[tile] = {
                "muro": muro,
                "muro_v": pygame.transform.rotate(muro, 90),
                "puerta": esc(self._img_puerta),
                "llave": esc(self._img_llave),
                "salida": esc(self._img_salida),
            }

        return self._cache_tiles[tile]

    def renderizar_mapa(
        self, pantalla, matriz, tile=TILE_SIZE, desplazamiento=(0, 0)
    ):
        pantalla.fill(NEGRO)

        ox, oy = desplazamiento
        img = self._imagenes(tile)
        k = tile / 40  # factor de escala de los iconos dibujados

        def p(px, py, x, y):
            return (x + px * k, y + py * k)

        for fila in range(len(matriz)):
            for col in range(len(matriz[fila])):
                casilla = matriz[fila][col]

                x = ox + col * tile
                y = oy + fila * tile

                if casilla == 1:
                    pantalla.blit(img["muro"], (x, y))

                elif casilla == 5:
                    pantalla.blit(img["muro_v"], (x, y))

                elif casilla == 2:
                    pantalla.blit(img["puerta"], (x, y))

                elif casilla == 3:
                    pantalla.blit(img["llave"], (x, y))

                elif casilla == 4:
                    pantalla.blit(img["salida"], (x, y))

                elif casilla == 6:
                    # Pocion azul
                    pygame.draw.circle(
                        pantalla, (40, 180, 255),
                        p(20, 23, x, y), max(2, int(12 * k))
                    )

                    pygame.draw.rect(
                        pantalla, (180, 230, 255),
                        (x + 16 * k, y + 7 * k, 8 * k, 8 * k)
                    )

                elif casilla == 7:
                    # Escudo verde
                    puntos = [
                        p(20, 5, x, y), p(33, 11, x, y),
                        p(30, 27, x, y), p(20, 35, x, y),
                        p(10, 27, x, y), p(7, 11, x, y)
                    ]

                    pygame.draw.polygon(
                        pantalla, (50, 220, 100), puntos
                    )

                    pygame.draw.polygon(
                        pantalla, BLANCO, puntos, 2
                    )

                elif casilla == 8:
                    # Rayo amarillo
                    puntos = [
                        p(23, 4, x, y), p(12, 21, x, y),
                        p(20, 21, x, y), p(16, 36, x, y),
                        p(29, 16, x, y), p(21, 16, x, y)
                    ]

                    pygame.draw.polygon(
                        pantalla, (255, 220, 40), puntos
                    )

    def dibujar_iluminacion(
        self, pantalla, jugador_x, jugador_y,
        tile=TILE_SIZE, desplazamiento=(0, 0)
    ):
        ox, oy = desplazamiento

        self.capa_oscuridad.fill(
            (0, 0, 0, self.alfa_oscuridad)
        )

        centro_x = ox + jugador_x * tile + tile // 2
        centro_y = oy + jugador_y * tile + tile // 2

        pygame.draw.circle(
            self.capa_oscuridad,
            (0, 0, 0, 0),
            (centro_x, centro_y),
            int(self.radio_luz * tile)
        )

        pantalla.blit(self.capa_oscuridad, (0, 0))

    def dibujar_menu_inicio(self, pantalla):
        pantalla.fill((15, 15, 22))

        raton = pygame.mouse.get_pos()

        fuente = pygame.font.SysFont(None, 56)
        titulo = fuente.render(
            "ESCAPE DE LA MAZMORRA", True, BLANCO
        )

        pantalla.blit(
            titulo,
            (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 3 - 30)
        )

        color = (
            (50, 180, 240)
            if self.rect_jugar.collidepoint(raton)
            else (30, 110, 160)
        )

        pygame.draw.rect(
            pantalla, color, self.rect_jugar, border_radius=12
        )

        fuente_boton = pygame.font.SysFont(None, 42)
        texto = fuente_boton.render("JUGAR", True, BLANCO)

        pantalla.blit(
            texto,
            (
                self.rect_jugar.centerx - texto.get_width() // 2,
                self.rect_jugar.centery - texto.get_height() // 2
            )
        )

    def dibujar_menu_dificultad(self, pantalla):
        pantalla.fill((15, 15, 22))

        raton = pygame.mouse.get_pos()

        fuente = pygame.font.SysFont(None, 48)
        titulo = fuente.render(
            "SELECCIONA LA DIFICULTAD", True, BLANCO
        )

        pantalla.blit(
            titulo,
            (WIDTH // 2 - titulo.get_width() // 2, 100)
        )

        fuente_boton = pygame.font.SysFont(None, 38)

        opciones = [
            ("Facil", self.rect_facil, (25, 130, 65), (40, 200, 100)),
            ("Normal", self.rect_normal, (150, 120, 30), (220, 180, 50)),
            ("Dificil", self.rect_dificil, (150, 35, 35), (230, 60, 60))
        ]

        for nombre, rect, normal, hover in opciones:
            color = hover if rect.collidepoint(raton) else normal

            pygame.draw.rect(
                pantalla, color, rect, border_radius=12
            )

            texto = fuente_boton.render(
                nombre, True, BLANCO
            )

            pantalla.blit(
                texto,
                (
                    rect.centerx - texto.get_width() // 2,
                    rect.centery - texto.get_height() // 2
                )
            )

    def configurar_dificultad(
        self, nuevo_radio_luz, nuevo_alfa_oscuridad=180
    ):
        # nuevo_radio_luz esta en casillas
        self.radio_luz = nuevo_radio_luz
        self.alfa_oscuridad = nuevo_alfa_oscuridad

    def _dibujar_corazon(self, pantalla, x, y, lleno):
        color = (230, 40, 60) if lleno else (70, 70, 80)

        pygame.draw.circle(pantalla, color, (x + 6, y + 6), 6)
        pygame.draw.circle(pantalla, color, (x + 16, y + 6), 6)
        pygame.draw.polygon(
            pantalla, color, [(x, y + 8), (x + 22, y + 8), (x + 11, y + 22)]
        )

    def dibujar_hud(
        self, pantalla, llaves, vidas=0, vidas_max=3,
        nivel_actual=1, total_niveles=1
    ):
        # Llaves (arriba a la izquierda)
        fondo = pygame.Surface((100, 35), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 180))

        pantalla.blit(fondo, (10, 10))
        pantalla.blit(self.img_llave_hud, (15, 15))

        texto = self.fuente_hud.render(
            f"x {llaves}", True, BLANCO
        )

        pantalla.blit(texto, (48, 17))

        # Nivel (arriba al centro)
        texto_nivel = self.fuente_hud.render(
            f"NIVEL {nivel_actual}/{total_niveles}", True, BLANCO
        )

        ancho = texto_nivel.get_width() + 24
        fondo_nivel = pygame.Surface((ancho, 35), pygame.SRCALPHA)
        fondo_nivel.fill((0, 0, 0, 180))

        x_nivel = WIDTH // 2 - ancho // 2
        pantalla.blit(fondo_nivel, (x_nivel, 10))
        pantalla.blit(texto_nivel, (x_nivel + 12, 17))

        # Vidas (arriba a la derecha)
        ancho_vidas = vidas_max * 30 + 10
        fondo_vidas = pygame.Surface((ancho_vidas, 35), pygame.SRCALPHA)
        fondo_vidas.fill((0, 0, 0, 180))

        x_vidas = WIDTH - ancho_vidas - 10
        pantalla.blit(fondo_vidas, (x_vidas, 10))

        for i in range(vidas_max):
            self._dibujar_corazon(
                pantalla, x_vidas + 8 + i * 30, 17, i < vidas
            )
