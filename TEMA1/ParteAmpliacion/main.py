import button as button
from colorama import init, Fore
from pygame import RLEACCEL

if __name__ == '__main__':
    # Import the pygame module
    import pygame
    # Import random for random numbers
    import random

    # Initialize pygame
    pygame.init()

    # Import pygame.locals for easier access to key coordinates
    # Updated to conform to flake8 and black standards
    from pygame.locals import (
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        K_m,
        QUIT
    )


    # Define a Player object by extending pygame.sprite.Sprite
    # The surface drawn on the screen is now an attribute of 'player'
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load("jet.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()

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

            # Keep player on the screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT


    # Define the enemy object by extending pygame.sprite.Sprite
    # The surface you draw on the screen is now an attribute of 'enemy'
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.image.load("missile.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.speed = random.randint(5, 20)

        # Move the sprite based on speed
        # Remove the sprite when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()


    # Creating cloud class
    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load("cloud.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.speed = random.randint(5, 20)

        def update(self):
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()


    def pausa(letras, gameDisplay):
        #pausa = true
        pauseText = pygame.font.SysFont(115)
        TextSurf, TextRect = letras("Pausa", pauseText)
        TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
        gameDisplay.blit(TextSurf, TextRect)


    # Define constants for the screen width and height
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a custom event for adding a new enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)

    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
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

    # Variable to keep the main loop running
    running = True

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

            if event.type == KEYDOWN:
                if event.key == K_m:
                    pygame.quit()
                    quit()

                    # Para poner el fondo blanco cuando pulsas pausa
                    # gameDisplay.fill(white)

                    # botones de continuar y salir
                    # button("Continuar?", 150, 450, 100, 50, Fore.green, Fore.bright_green, true)
                button("Quit", 550, 450, 100, 50, Fore.red, Fore.bright_red, QUIT)

            elif event.type == QUIT:
                running = False
            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            # Add a new cloud
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # update cloud position
        clouds.update()

        # Update enemy position
        enemies.update()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        # Fill the screen with black
        screen.fill((135, 206, 250))

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            collision_sound.play()
            player.kill()
            running = False

        # Update the display
        pygame.display.flip()

        clock.tick(60)

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
