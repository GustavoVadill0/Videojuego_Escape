
import pygame
import os


class SistemaSonido:

    def __init__(self):
        self.disponible = False
        self.sonidos = {}
        self.canal_movimiento = None
        self.canal_efectos = None
        self.ruta_musica = os.path.join(
            "assets", "sonidos", "musica_mazmorra.mp3"
        )

        carpeta = os.path.join("assets", "sonidos")

        archivos = {
            "movimiento": "soumages-running-363346.mp3",
            "llave": "llave.mp3",
            "poder": "sonido_poder.mp3",
            "victoria": "victoria.mp3",
            "derrota": "derrota.mp3"
        }

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.set_num_channels(8)

            self.canal_movimiento = pygame.mixer.Channel(0)
            self.canal_efectos = pygame.mixer.Channel(1)

            for nombre, archivo in archivos.items():
                ruta = os.path.join(carpeta, archivo)

                if os.path.exists(ruta):
                    sonido = pygame.mixer.Sound(ruta)
                    sonido.set_volume(0.5)
                    self.sonidos[nombre] = sonido
                else:
                    print("No se encontro el archivo:", ruta)

            self.disponible = True

        except pygame.error as error:
            print("Error al iniciar el audio:", error)

    def reproducir_movimiento(self):
        if not self.disponible:
            return

        sonido = self.sonidos.get("movimiento")

        if sonido and not self.canal_movimiento.get_busy():
            self.canal_movimiento.play(sonido)

    def detener_movimiento(self):
        if self.canal_movimiento:
            self.canal_movimiento.stop()

    def reproducir_efecto(self, nombre):
        if not self.disponible:
            return

        sonido = self.sonidos.get(nombre)

        if sonido:
            self.canal_efectos.stop()
            self.canal_efectos.play(sonido)

    def iniciar_musica(self):
        if not self.disponible:
            return

        if not os.path.exists(self.ruta_musica):
            print("No se encontro la musica:", self.ruta_musica)
            return

        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.ruta_musica)
                pygame.mixer.music.set_volume(0.50)
                pygame.mixer.music.play(-1)
        except pygame.error as error:
            print("No se pudo reproducir la musica:", error)

    def detener_musica(self):
        if self.disponible:
            pygame.mixer.music.stop()

    def reproducir_llave(self):
        self.reproducir_efecto("llave")

    def reproducir_poder(self):
        self.reproducir_efecto("poder")

    def reproducir_victoria(self):
        self.detener_movimiento()
        self.detener_musica()
        self.reproducir_efecto("victoria")

    def reproducir_derrota(self):
        self.detener_movimiento()
        self.detener_musica()
        self.reproducir_efecto("derrota")
