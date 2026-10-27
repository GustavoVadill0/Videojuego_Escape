
import pygame
from config import *


class MotorVisual:

    def __init__(self, ancho, alto):
        self.capa_oscuridad = pygame.Surface(
            (ancho, alto), pygame.SRCALPHA
        )

        self.radio_luz = TILE_SIZE * 3
        self.alfa_oscuridad = 180

        def cargar_tile(ruta):
            img = pygame.image.load(
                ruta
            ).convert_alpha()

            return pygame.transform.scale(
                img, (TILE_SIZE, TILE_SIZE)
            )

        self.img_muro = cargar_tile("assets/muro.png")
        self.img_muro_v = pygame.transform.rotate(
            self.img_muro, 90
        )
        self.img_puerta = cargar_tile("assets/puerta.png")
        self.img_llave = cargar_tile("assets/llave.png")
        self.img_salida = cargar_tile("assets/salida.png")

        self.fuente_hud = pygame.font.SysFont(None, 32)
        self.img_llave_hud = pygame.transform.scale(
            self.img_llave, (25, 25)
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

    def renderizar_mapa(self, pantalla, matriz):
        pantalla.fill(NEGRO)

        for fila in range(len(matriz)):
            for col in range(len(matriz[fila])):
                casilla = matriz[fila][col]

                x = col * TILE_SIZE
                y = fila * TILE_SIZE

                if casilla == 1:
                    pantalla.blit(self.img_muro, (x, y))

                elif casilla == 5:
                    pantalla.blit(self.img_muro_v, (x, y))

                elif casilla == 2:
                    pantalla.blit(self.img_puerta, (x, y))

                elif casilla == 3:
                    pantalla.blit(self.img_llave, (x, y))

                elif casilla == 4:
                    pantalla.blit(self.img_salida, (x, y))

                elif casilla == 6:
                    # Pocion azul
                    pygame.draw.circle(
                        pantalla, (40, 180, 255),
                        (x + 20, y + 23), 12
                    )

                    pygame.draw.rect(
                        pantalla, (180, 230, 255),
                        (x + 16, y + 7, 8, 8)
                    )

                elif casilla == 7:
                    # Escudo verde
                    puntos = [
                        (x + 20, y + 5),
                        (x + 33, y + 11),
                        (x + 30, y + 27),
                        (x + 20, y + 35),
                        (x + 10, y + 27),
                        (x + 7, y + 11)
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
                        (x + 23, y + 4),
                        (x + 12, y + 21),
                        (x + 20, y + 21),
                        (x + 16, y + 36),
                        (x + 29, y + 16),
                        (x + 21, y + 16)
                    ]

                    pygame.draw.polygon(
                        pantalla, (255, 220, 40), puntos
                    )

    def dibujar_iluminacion(self, pantalla, jugador_x, jugador_y):
        self.capa_oscuridad.fill(
            (0, 0, 0, self.alfa_oscuridad)
        )

        centro_x = jugador_x * TILE_SIZE + TILE_SIZE // 2
        centro_y = jugador_y * TILE_SIZE + TILE_SIZE // 2

        pygame.draw.circle(
            self.capa_oscuridad,
            (0, 0, 0, 0),
            (centro_x, centro_y),
            self.radio_luz
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
        self.radio_luz = nuevo_radio_luz
        self.alfa_oscuridad = nuevo_alfa_oscuridad

    def dibujar_hud(self, pantalla, llaves):
        fondo = pygame.Surface((100, 35), pygame.SRCALPHA)
        fondo.fill((0, 0, 0, 180))

        pantalla.blit(fondo, (10, 10))
        pantalla.blit(self.img_llave_hud, (15, 15))

        texto = self.fuente_hud.render(
            f"x {llaves}", True, BLANCO
        )

        pantalla.blit(texto, (48, 17))
