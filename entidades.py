import pygame
from config import TILE_SIZE

class Entidad:
    def __init__(self, x, y, ruta_imagen):
        self.x = x
        self.y = y
        imagen_bruta = pygame.image.load(ruta_imagen).convert_alpha()
        self.imagen = pygame.transform.scale(imagen_bruta, (TILE_SIZE, TILE_SIZE))

    def dibujar(self, superficie):
        superficie.blit(self.imagen, (self.x * TILE_SIZE, self.y * TILE_SIZE))

class Jugador(Entidad):
    def __init__(self):
        super().__init__(1, 5, "assets/jugador.png")

    def reiniciar(self):
        self.x = 1
        self.y = 5

    def mover(self, dx, dy, nivel):
        nx, ny = self.x + dx, self.y + dy
        destino = nivel.matriz[ny][nx]

        if destino == 0 or destino == 4:
            self.x, self.y = nx, ny
            return True
        elif destino == 3:
            nivel.llaves_recolectadas += 1
            nivel.matriz[ny][nx] = 0
            self.x, self.y = nx, ny
            return True
        elif destino == 2 and nivel.llaves_recolectadas > 0:
            nivel.llaves_recolectadas -= 1
            nivel.matriz[ny][nx] = 0
            self.x, self.y = nx, ny
            return True
        return False

class Monstruo(Entidad):
    def __init__(self):
        super().__init__(10, 5, "assets/monstruo.png")
        self.ultimo_movimiento = pygame.time.get_ticks()
        self.velocidad = 400

    def reiniciar(self):
        self.x = 10
        self.y = 5
        self.ultimo_movimiento = pygame.time.get_ticks()

    def configurar_velocidad(self, nueva_velocidad):
        self.velocidad = nueva_velocidad

    def cazar(self, jugador_x, jugador_y, nivel):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_movimiento > self.velocidad:
            self.x, self.y = nivel.bfs_pathfinding(self.x, self.y, jugador_x, jugador_y)
            self.ultimo_movimiento = ahora