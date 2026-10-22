import pygame
from config import *

class MotorVisual:
    def __init__(self, ancho, alto):
        self.capa_oscuridad = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        self.radio_luz = TILE_SIZE * 3
        self.alfa_oscuridad = 180

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
        self.capa_oscuridad.fill((0, 0, 0, self.alfa_oscuridad))
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
        pantalla.fill((15, 15, 22))
        pos_raton = pygame.mouse.get_pos()

        # Título principal
        fuente_titulo = pygame.font.SysFont(None, 56)
        titulo = fuente_titulo.render("ESCAPE DE LA MAZMORRA", True, BLANCO)
        pantalla.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 3 - 30))

        # Botón JUGAR
        self.rect_jugar = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2, 220, 55)
        col_jugar = (50, 180, 240) if self.rect_jugar.collidepoint(pos_raton) else (30, 110, 160)
        pygame.draw.rect(pantalla, col_jugar, self.rect_jugar, border_radius=12)

        fuente_btn = pygame.font.SysFont(None, 42)
        txt_jugar = fuente_btn.render("JUGAR", True, BLANCO)
        pantalla.blit(txt_jugar, (self.rect_jugar.centerx - txt_jugar.get_width() // 2, self.rect_jugar.centery - txt_jugar.get_height() // 2))

    def dibujar_menu_dificultad(self, pantalla):
        pantalla.fill((15, 15, 22))
        pos_raton = pygame.mouse.get_pos()

        # Título de dificultad
        fuente_titulo = pygame.font.SysFont(None, 48)
        titulo = fuente_titulo.render("SELECCIONA LA DIFICULTAD", True, BLANCO)
        pantalla.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 100))

        fuente_botones = pygame.font.SysFont(None, 38)

        # Botón Fácil
        self.rect_facil = pygame.Rect(WIDTH // 2 - 110, 190, 220, 50)
        col_facil = (40, 200, 100) if self.rect_facil.collidepoint(pos_raton) else (25, 130, 65)
        pygame.draw.rect(pantalla, col_facil, self.rect_facil, border_radius=12)
        txt_facil = fuente_botones.render("Fácil", True, BLANCO)
        pantalla.blit(txt_facil, (self.rect_facil.centerx - txt_facil.get_width() // 2, self.rect_facil.centery - txt_facil.get_height() // 2))

        # Botón Normal
        self.rect_normal = pygame.Rect(WIDTH // 2 - 110, 260, 220, 50)
        col_normal = (220, 180, 50) if self.rect_normal.collidepoint(pos_raton) else (150, 120, 30)
        pygame.draw.rect(pantalla, col_normal, self.rect_normal, border_radius=12)
        txt_normal = fuente_botones.render("Normal", True, BLANCO)
        pantalla.blit(txt_normal, (self.rect_normal.centerx - txt_normal.get_width() // 2, self.rect_normal.centery - txt_normal.get_height() // 2))

        # Botón Difícil
        self.rect_dificil = pygame.Rect(WIDTH // 2 - 110, 330, 220, 50)
        col_dificil = (230, 60, 60) if self.rect_dificil.collidepoint(pos_raton) else (150, 35, 35)
        pygame.draw.rect(pantalla, col_dificil, self.rect_dificil, border_radius=12)
        txt_dificil = fuente_botones.render("Difícil", True, BLANCO)
        pantalla.blit(txt_dificil, (self.rect_dificil.centerx - txt_dificil.get_width() // 2, self.rect_dificil.centery - txt_dificil.get_height() // 2))

    def configurar_dificultad(self, nuevo_radio_luz, nuevo_alfa_oscuridad=180):
        self.radio_luz = nuevo_radio_luz
        self.alfa_oscuridad = nuevo_alfa_oscuridad

    def dibujar_hud(self, pantalla, llaves):
        fondo_hud = pygame.Surface((100, 35), pygame.SRCALPHA)
        fondo_hud.fill((0, 0, 0, 180))
        pantalla.blit(fondo_hud, (10, 10))

        pantalla.blit(self.img_llave_hud, (15, 15))

        texto_llaves = self.fuente_hud.render(f"x {llaves}", True, BLANCO)
        pantalla.blit(texto_llaves, (48, 17))