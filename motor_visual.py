import pygame
from config import *

class MotorVisual:
    def __init__(self, ancho, alto):
        self.capa_oscuridad = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        self.radio_luz = TILE_SIZE * 3

        def cargar_tile(ruta):
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

        self.img_muro = cargar_tile("assets/muro.png")
        self.img_muro_v = pygame.transform.rotate(self.img_muro, 90)
        self.img_puerta = cargar_tile("assets/puerta.png")
        self.img_llave = cargar_tile("assets/llave.png")
        self.img_salida = cargar_tile("assets/salida.png")

        # Variables del HUD
        self.fuente_hud = pygame.font.SysFont(None, 32)
        self.img_llave_hud = pygame.transform.scale(self.img_llave, (25, 25))

    def renderizar_mapa(self, pantalla, matriz):
        pantalla.fill(NEGRO)

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                casilla = matriz[fila][col]
                x_pixel = col * TILE_SIZE
                y_pixel = fila * TILE_SIZE

                if casilla == 1:
                    pantalla.blit(self.img_muro, (x_pixel, y_pixel))
                elif casilla == 5:
                    pantalla.blit(self.img_muro_v, (x_pixel, y_pixel))
                elif casilla == 2:
                    pantalla.blit(self.img_puerta, (x_pixel, y_pixel))
                elif casilla == 3:
                    pantalla.blit(self.img_llave, (x_pixel, y_pixel))
                elif casilla == 4:
                    pantalla.blit(self.img_salida, (x_pixel, y_pixel))

    def dibujar_iluminacion(self, pantalla, jugador_x, jugador_y):
        self.capa_oscuridad.fill((0, 0, 0, 220))
        centro_x = (jugador_x * TILE_SIZE) + (TILE_SIZE // 2)
        centro_y = (jugador_y * TILE_SIZE) + (TILE_SIZE // 2)
        pygame.draw.circle(self.capa_oscuridad, (0, 0, 0, 0), (centro_x, centro_y), self.radio_luz)
        pantalla.blit(self.capa_oscuridad, (0, 0))

    def dibujar_interfaz_fin(self, pantalla, estado):
        fuente_grande = pygame.font.SysFont(None, 48)
        if estado == "GAME OVER":
            texto_fin = fuente_grande.render("¡TE ATRAPARON!", True, ROJO)
        else:
            texto_fin = fuente_grande.render("¡ESCAPASTE!", True, VERDE)

        pantalla.blit(texto_fin, (WIDTH//2 - 140, HEIGHT//2 - 40))

        rect_boton = pygame.Rect(BOTON_X, BOTON_Y, BOTON_ANCHO, BOTON_ALTO)
        pygame.draw.rect(pantalla, GRIS_CLARO, rect_boton)
        pygame.draw.rect(pantalla, BLANCO, rect_boton, 3)

        fuente_chica = pygame.font.SysFont(None, 36)
        texto_boton = fuente_chica.render("Jugar de nuevo", True, NEGRO)
        pantalla.blit(texto_boton, (BOTON_X + 15, BOTON_Y + 12))

    def dibujar_menu_inicio(self, pantalla):
        pantalla.fill((0, 0, 0))

        fuente_titulo = pygame.font.SysFont(None, 64)
        titulo = fuente_titulo.render("ESCAPE DE LA MAZMORRA", True, BLANCO)
        pantalla.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//4))

        fuente_botones = pygame.font.SysFont(None, 48)

        # Botón Fácil
        self.rect_facil = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
        pygame.draw.rect(pantalla, VERDE, self.rect_facil)
        texto_facil = fuente_botones.render("Fácil", True, NEGRO)
        pantalla.blit(texto_facil, (WIDTH//2 - texto_facil.get_width()//2, HEIGHT//2 - 50))

        # Botón Normal
        self.rect_normal = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 10, 200, 50)
        pygame.draw.rect(pantalla, BLANCO, self.rect_normal)
        texto_normal = fuente_botones.render("Normal", True, NEGRO)
        pantalla.blit(texto_normal, (WIDTH//2 - texto_normal.get_width()//2, HEIGHT//2 + 20))

        # Botón Difícil
        self.rect_dificil = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)
        pygame.draw.rect(pantalla, ROJO, self.rect_dificil)
        texto_dificil = fuente_botones.render("Difícil", True, NEGRO)
        pantalla.blit(texto_dificil, (WIDTH//2 - texto_dificil.get_width()//2, HEIGHT//2 + 90))

    def configurar_dificultad(self, nuevo_radio_luz):
        self.radio_luz = nuevo_radio_luz

    def dibujar_hud(self, pantalla, llaves):
        fondo_hud = pygame.Surface((100, 35), pygame.SRCALPHA)
        fondo_hud.fill((0, 0, 0, 180))
        pantalla.blit(fondo_hud, (10, 10))

        pantalla.blit(self.img_llave_hud, (15, 15))

        texto_llaves = self.fuente_hud.render(f"x {llaves}", True, BLANCO)
        pantalla.blit(texto_llaves, (48, 17))