import pygame
import random
import sys
import os

ANCHO = 400
ALTO = 600

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

VEL_MOVIMIENTO = 5
VEL_DISPARO = 10
VEL_ENEMIGO = 3

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Impact")

pygame.mixer.music.load(os.path.join("sounds", "sound.mp3"))
pygame.mixer.music.play(-1)

fondo = pygame.image.load(os.path.join("img", "fondo.jpg"))
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))


def cargar_imagen(nombre_archivo):
    ruta = os.path.join("img", nombre_archivo)
    imagen = pygame.image.load(ruta)
    imagen = pygame.transform.scale(imagen, (50, 50))
    return imagen


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cargar_imagen("1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20
        self.disparos = pygame.sprite.Group()

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= VEL_MOVIMIENTO
        if teclas[pygame.K_RIGHT]:
            self.rect.x += VEL_MOVIMIENTO
        if teclas[pygame.K_UP]:
            self.rect.y -= VEL_MOVIMIENTO
        if teclas[pygame.K_DOWN]:
            self.rect.y += VEL_MOVIMIENTO
        self.rect.x = max(0, min(self.rect.x, ANCHO - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTO - self.rect.height))

        if teclas[pygame.K_SPACE]:
            self.disparar()

        self.disparos.update()

    def disparar(self):
        disparo = Disparo(self.rect.centerx, self.rect.top)
        self.disparos.add(disparo)


class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3, 10))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= VEL_DISPARO
        if self.rect.bottom < 0:
            self.kill()


class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cargar_imagen("2.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, ANCHO - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += VEL_ENEMIGO
        if self.rect.top > ALTO:
            self.kill()


def crear_enemigos(grupo_enemigos):
    enemigo = Enemigo()
    grupo_enemigos.add(enemigo)


def main():
    nave = Nave()
    grupo_enemigos = pygame.sprite.Group()
    grupo_disparos = nave.disparos
    reloj = pygame.time.Clock()
    tiempo_creacion_enemigo = 0
    juego_activo = False
    puntuacion = 0

    font_inicio = pygame.font.Font(None, 36)
    texto_inicio1 = font_inicio.render("Space Impact", True, BLANCO)
    texto_inicio2 = font_inicio.render(
        "Presiona ESPACIO para empezar", True, BLANCO)
    texto_rect1 = texto_inicio1.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    texto_rect2 = texto_inicio2.get_rect(center=(ANCHO // 2, ALTO // 2))

    while not juego_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    juego_activo = True

        ventana.fill(NEGRO)
        ventana.blit(texto_inicio1, texto_rect1)
        ventana.blit(texto_inicio2, texto_rect2)
        pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if juego_activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_creacion_enemigo > 1000:
                crear_enemigos(grupo_enemigos)
                tiempo_creacion_enemigo = tiempo_actual

            nave.update()
            grupo_disparos.update()
            grupo_enemigos.update()

            colisiones_disparos_enemigos = pygame.sprite.groupcollide(
                grupo_disparos, grupo_enemigos, True, True)
            puntuacion += len(colisiones_disparos_enemigos)

            if pygame.sprite.spritecollide(nave, grupo_enemigos, False):
                juego_activo = False

            ventana.blit(fondo, (0, 0))
            ventana.blit(nave.image, nave.rect)
            grupo_disparos.draw(ventana)
            grupo_enemigos.draw(ventana)

            font = pygame.font.Font(None, 36)
            texto_puntuacion = font.render(
                f"Puntuación: {puntuacion}", True, BLANCO)
            ventana.blit(texto_puntuacion, (10, 10))

        else:
            ventana.fill(NEGRO)
            font = pygame.font.Font(None, 48)
            texto_game_over = font.render("Game Over", True, BLANCO)
            texto_rect = texto_game_over.get_rect(
                center=(ANCHO // 2, ALTO // 2))
            ventana.blit(texto_game_over, texto_rect)

        pygame.display.flip()
        reloj.tick(30)


if __name__ == "__main__":
    main()
