import os
import sqlite3
from sqlite3 import Error

from pygame import RLEACCEL

if __name__ == '__main__':
    # Import the pygame module
    import pygame
    # Import random for random numbers
    import random
    # Import pygame.locals for easier access to key coordinates
    # Updated to conform to flake8 and black standards
    from pygame.locals import (
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        K_p,
        K_m,
        K_SPACE,
        QUIT
    )

    # Initialize pygame
    pygame.init()

    score = 0
    nivel = 1
    # rutas
    directorio_carpeta = os.path.dirname(__file__)
    ruta_max_score = os.path.join(directorio_carpeta, "puntuacion.db")


    # Define a Player object by extending pygame.sprite.Sprite
    # The surface drawn on the screen is now an attribute of 'player'

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load("diminisher.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()
            # Velocidad de lanzamiento de los misiles
            self.velLanzamiento = 600
            self.last_misil = pygame.time.get_ticks()

        # Move the sprite based on user keypresses
        def update(self, pressed_keys):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
            if pressed_keys[K_SPACE]:
                action = pygame.time.get_ticks()  # Momento en el que la nave dispara
                if action - self.last_misil > self.velLanzamiento:
                    self.disparoMisil()
                    self.last_misil = action

            # Keep player on the screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

        def disparoMisil(self):
            municion = Misiles(self.rect.centerx, self.rect.centery)
            misil.add(municion)

    class Misiles(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super(Misiles, self).__init__()
            self.image = pygame.image.load(("missile.png")).convert()
            self.image.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.image.get_rect()
            self.rect.centerx = x + 10
            self.rect.bottom = y

        def update(self):
            self.rect.x += 15
            if self.rect.bottom < SCREEN_WIDTH:
                self.kill()


    # Define the enemy object by extending pygame.sprite.Sprite
    # The surface you draw on the screen is now an attribute of 'enemy'
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            if background == True:
                self.surf = pygame.image.load("misile_v1.png").convert()  # De dia misil
            elif background == False:
                self.surf = pygame.image.load("alien_green.png").convert()  # De noche aliens
                self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.speed = random.randint(2 * nivel, 10 + 3 * nivel)
            # velocidad enemigos

        # Move the sprite based on speed
        # Remove the sprite when it passes the left edge of the screen
        def update(self):
            global score
            global nivel
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                for e in enemies:
                    if e.rect.right <= 1:
                        score += 10
                        if score % 500 == 0:
                            nivel += 1
                self.kill()


    # Creating cloud class

    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            if background == True:
                self.surf = pygame.image.load("nube_v1.png").convert()  # De dia nubes
            elif background == False:
                self.surf = pygame.image.load("estrella.png").convert()  # De noches "estrellas"
                self.surf.set_colorkey((255, 255, 255), RLEACCEL)

            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 60, SCREEN_WIDTH + 150),
                    random.randint(20, SCREEN_HEIGHT)
                )
            )

        def update(self):
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()



    # Primer ejercicio y nivel
    def marcador(surface, text, text2, size, x, y):
        font = pygame.font.SysFont("serif", size)  # fuente del marcador
        text_surface = font.render("{} : {}".format(text, text2), True,
                                   (50, 50, 100))  # color y tamaño de la letra
        text_rect = text_surface.get_rect()
        text_rect.midright = (x, y)
        surface.blit(text_surface, text_rect)


    # Parte SQL
    # Python tiene implementados metodos propios para la conexion SQL pero ya habia creado las definiciones

    # Conexion DB
    def connexion():
        try:
            sqliteConnection = sqlite3.connect((os.path.join(ruta_max_score)))
            return sqliteConnection
        except Error:
            print(Error)


    con = connexion()


    # insertar datos para nueva puntuacion
    def sql_insert(score):
        cursorobj = con.cursos()
        if leersql() == 0:
            cursorobj.execute(
                'INSERT INTO puntuacion VALUES({})'.format(score))
        if leersql > score:
            return
        else:
            updatesql()

        con.comit()


    def leersql():
        cursor = con.cursor()
        cursor.execute("SELECT score FROM puntuacion")
        row = cursor.fetchone()
        return row[0]


    # Actualizamos el score con la puntuacion mas alta,
    # si en la partida actual la puntuacion no supera a la puntuacion guardada no se sobreescribiria
    def updatesql():
        curs = con.cursor()
        if leersql() > score:
            print("Puntuacion actual"
                  + "\n--------------------------------------------"
                  + "\n>>>>: " + str(score)
                  + "\n--------------------------------------------"
                  )
        if leersql() < score:
            curs.execute("Update puntuacion set score = " + str(score))
            print("Nueva puntuacion mas alta: ", score)
            curs.execute("select * from puntuacion")
            con.commit()

# Define constants for the screen width and height
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fondo oscuro
modo_noche = pygame.image.load("nightmode.png")

# Fondo de dia
modo_dia = pygame.image.load("daymode.png")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
# UPDATE ENEMY
velEne = int(200 + (150 / nivel))
pygame.time.set_timer(ADDENEMY, velEne)

# Aparicion de objetos que no eliminan al jugador
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Cambio de fondo del juego
ADDTIME = pygame.USEREVENT + 3
pygame.time.set_timer(ADDTIME, 10000)

ADDMISIL = pygame.USEREVENT + 4
pygame.time.set_timer(ADDMISIL, 2000)

rgb_current = (135, 206, 250)
background = True

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
misil = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Setup fr sounds.Default are good.
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("Apoxode_-_Electric_1.ogg")
pygame.mixer.music.play(loops=-1)  # Se reproduzca infinitamente

# Load all sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

move_down_sound.set_volume(0.1)
move_up_sound.set_volume(0.1)
collision_sound.set_volume(0.1)
pygame.mixer.music.set_volume(0.1)  # volumen del juego

font_intro = pygame.font.SysFont("serif", 30)

intro = True
end = True
running = True

# Menu intro
while intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill((253, 253, 150))

    intro_label = font_intro.render("Press p to play", 1, (0, 0, 0))
    screen.blit(intro_label, (600, 200))

    ult_score = font_intro.render(f"Puntuacion mas alta: {leersql()}", 1, (0, 0, 0))
    screen.blit(ult_score, (600, 300))  # el primero es Y y el segundo es X

    salir = font_intro.render("Pulsa ESC para salir del juego", 1, (0, 0, 0))
    screen.blit(salir, (20, 20))

    tecla = pygame.key.get_pressed()

    if tecla[pygame.K_p]:
        intro = False
    if tecla[pygame.K_ESCAPE]:
        intro = False
        running = False
    pygame.display.update()

# Variable to keep the main loop running
# Main loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == KEYDOWN:
            # if the UP_KEY is pressed, then it will sound the up sound
            if event.key == K_UP:
                move_up_sound.play()

        if event.type == KEYDOWN:
            # if the DOWN_KEY is pressed, then it will sound the up sound
            if event.key == K_DOWN:
                move_down_sound.play()

        elif event.type == QUIT:
            running = False
        # Add a new enemy
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new background
        elif event.type == ADDTIME:
            if background is False:  # dia
                background = True
                rgb_current = (135, 206, 250)
                # screen.blit(modo_noche, (0, 0))
            elif background is True:  # noche
                background = False
                rgb_current = (37, 40, 80)
                # screen.blit(modo_dia, (0, 0))
        # Add a new cloud
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    screen.fill(rgb_current)

# Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # update cloud position
    clouds.update()

    # Update enemy position
    enemies.update()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # COLISION
    choque = pygame.sprite.groupcollide(misil, enemies, True, True)

    # Acumulador de puntos cuando un misil impacta con un enemigo
    if choque:
        score += 10

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):

        # verlo en consola
        # If so, then remove the player and stop the loop
        collision_sound.play()
        connexion()
        print("\n--------------------------------------------")
        print("Puntuacion mas alta", leersql())
        print("--------------------------------------------")
        updatesql()
        player.kill()

        # menu final
        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            screen.fill((0, 0, 0))
            intro_label = font_intro.render("GAME OVER", 1, (110, 110, 110))
            screen.blit(intro_label, (600, 200))

            ult_score = font_intro.render(f"Ultima puntuacion:{leersql()}", 1, (110, 110, 110))
            screen.blit(ult_score, (600, 300))  # el primero es Y y el segundo es X

            puntuacion_actual = font_intro.render(f"Score en esta partida:{score}", 1, (110, 110, 110))
            screen.blit(puntuacion_actual, (600, 400))

            salir = font_intro.render("Pulsa ESC para salir del juego", 1, (110, 110, 110))
            screen.blit(salir, (20, 20))

            tecla = pygame.key.get_pressed()

            if tecla[pygame.K_ESCAPE] or tecla[pygame.K_p]:
                end = False
            pygame.display.update()

        running = False
        pygame.display.update()

    marcador(screen, "Score ", str(score), 35, 1870, 30)
    marcador(screen, "Nivel ", str(nivel), 35, 1870, 80)

    # Update the display
    pygame.display.flip()

    clock.tick(60)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
