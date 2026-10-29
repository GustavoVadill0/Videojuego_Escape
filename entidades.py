
import pygame
from config import TILE_SIZE


class Entidad:

    def __init__(self, x, y, ruta_imagen):
        self.x = x
        self.y = y

        imagen_bruta = pygame.image.load(
            ruta_imagen
        ).convert_alpha()

        self.imagen_original = pygame.transform.scale(
            imagen_bruta, (TILE_SIZE, TILE_SIZE)
        )

        self.orientacion = "DERECHA"

        self.sprites = {
            "DERECHA": self.imagen_original,
            "IZQUIERDA": pygame.transform.flip(
                self.imagen_original, True, False
            ),
            "ARRIBA": pygame.transform.rotate(
                self.imagen_original, 90
            ),
            "ABAJO": pygame.transform.rotate(
                self.imagen_original, -90
            )
        }

    def dibujar(self, superficie):
        superficie.blit(
            self.sprites[self.orientacion],
            (self.x * TILE_SIZE, self.y * TILE_SIZE)
        )


class Jugador(Entidad):

    def __init__(self):
        super().__init__(1, 5, "assets/jugador.png")

        self.escudo_activo = False
        self.fin_aceleracion = 0

    def reiniciar(self):
        self.x = 1
        self.y = 5
        self.orientacion = "DERECHA"
        self.escudo_activo = False
        self.fin_aceleracion = 0

    def mover(self, dx, dy, nivel):
        if dx > 0:
            self.orientacion = "DERECHA"
        elif dx < 0:
            self.orientacion = "IZQUIERDA"
        elif dy < 0:
            self.orientacion = "ARRIBA"
        elif dy > 0:
            self.orientacion = "ABAJO"

        nx = self.x + dx
        ny = self.y + dy

        # Evitar salir de los limites de la matriz
        if not (
            0 <= ny < len(nivel.matriz)
            and 0 <= nx < len(nivel.matriz[0])
        ):
            return False

        destino = nivel.matriz[ny][nx]

        # Caminar por una casilla vacia o llegar a la salida
        if destino == 0 or destino == 4:
            self.x, self.y = nx, ny
            return True

        # Recoger una llave
        elif destino == 3:
            nivel.llaves_recolectadas += 1
            nivel.matriz[ny][nx] = 0
            self.x, self.y = nx, ny
            return "llave"

        # Abrir una puerta utilizando una llave
        elif destino == 2 and nivel.llaves_recolectadas > 0:
            nivel.llaves_recolectadas -= 1
            nivel.matriz[ny][nx] = 0
            self.x, self.y = nx, ny
            return True

        # Recoger cualquiera de los tres poderes
        elif destino in (6, 7, 8):
            nivel.poderes_pendientes.append(destino)
            nivel.matriz[ny][nx] = 0
            self.x, self.y = nx, ny
            return True

        # No se pudo avanzar
        return False


class Monstruo(Entidad):

    def __init__(self):
        super().__init__(10, 5, "assets/monstruo.png")

        self.ultimo_movimiento = pygame.time.get_ticks()
        self.velocidad_normal = 400
        self.velocidad = 400
        self.fin_ralentizacion = 0

    def reiniciar(self):
        self.x = 10
        self.y = 5
        self.orientacion = "DERECHA"
        self.ultimo_movimiento = pygame.time.get_ticks()
        self.velocidad = self.velocidad_normal
        self.fin_ralentizacion = 0

    def configurar_velocidad(self, nueva_velocidad):
        self.velocidad_normal = nueva_velocidad
        self.velocidad = nueva_velocidad
        self.fin_ralentizacion = 0

    def activar_ralentizacion(self):
        ahora = pygame.time.get_ticks()

        self.velocidad = self.velocidad_normal * 2
        self.fin_ralentizacion = ahora + 5000

    def cazar(self, jugador_x, jugador_y, nivel):
        ahora = pygame.time.get_ticks()

        # Restaurar velocidad cuando termina el poder
        if (
            self.fin_ralentizacion > 0
            and ahora >= self.fin_ralentizacion
        ):
            self.velocidad = self.velocidad_normal
            self.fin_ralentizacion = 0

        if ahora - self.ultimo_movimiento >= self.velocidad:
            nx, ny = nivel.bfs_pathfinding(
                self.x, self.y, jugador_x, jugador_y
            )

            dx = nx - self.x
            dy = ny - self.y

            if dx > 0:
                self.orientacion = "DERECHA"
            elif dx < 0:
                self.orientacion = "IZQUIERDA"
            elif dy < 0:
                self.orientacion = "ARRIBA"
            elif dy > 0:
                self.orientacion = "ABAJO"

            self.x, self.y = nx, ny
            self.ultimo_movimiento = ahora
