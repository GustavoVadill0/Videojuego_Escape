import pygame
from config import *

class MotorVisual:
    def __init__(self, ancho, alto):
        self.capa_oscuridad = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        self.radio_luz = TILE_SIZE * 3  
        
        # Función auxiliar para evitar repetir código al cargar texturas del entorno
        def cargar_tile(ruta):
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            
        self.img_muro = cargar_tile("assets/muro.png")
        self.img_muro_v = pygame.transform.rotate(self.img_muro, 90)
        self.img_puerta = cargar_tile("assets/puerta.png")
        self.img_llave = cargar_tile("assets/llave.png")
        self.img_salida = cargar_tile("assets/salida.png")

    def renderizar_mapa(self, pantalla, matriz):
        pantalla.fill(NEGRO) # El suelo libre se queda de color negro
        
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                casilla = matriz[fila][col]
                x_pixel = col * TILE_SIZE
                y_pixel = fila * TILE_SIZE
                
                if casilla == 1:
                    pantalla.blit(self.img_muro, (x_pixel, y_pixel))
                elif casilla == 5: # Muro Vertical (NUEVO)
                    pantalla.blit(self.img_muro_v, (x_pixel, y_pixel))
                elif casilla == 2:
                    pantalla.blit(self.img_puerta, (x_pixel, y_pixel))
                elif casilla == 3:
                    pantalla.blit(self.img_llave, (x_pixel, y_pixel))
                elif casilla == 4:
                    pantalla.blit(self.img_salida, (x_pixel, y_pixel))

    def dibujar_iluminacion(self, pantalla, jugador_x, jugador_y):
        self.capa_oscuridad.fill((0, 0, 0, 240))
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