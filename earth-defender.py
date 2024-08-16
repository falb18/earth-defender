import pygame
import math

from constants import *
from objects import *

DELAY_BEFORE_SPAWN_ASTEROID_MS = 3000

# Window settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
FPS = 60 # frames per second

#------------------------------------------------------------------------------
# Game init:
#------------------------------------------------------------------------------

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_radius = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2)/2
pygame.display.set_caption("Earth Defender")

# Create game objects
spaceship = Spaceship(SCREEN_CENTER)
earth = Earth(SCREEN_CENTER)

sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
asteroid_sprites = pygame.sprite.Group()

sprites.add(spaceship, earth)

#------------------------------------------------------------------------------
# Game functions:
#------------------------------------------------------------------------------

def check_bullets_position():
    """
    The function checks if any of the bullets is outside the screen. In case one or more
    bullets are outside the screen then it deletes them from the bullets_sprites group.
    This function has to be called before checking the collision between the bullets and
    the asteroids.
    """
    offset = 10
    bullets = bullet_sprites.sprites()
    for bullet in bullets:
        if (bullet.rect.centerx > SCREEN_WIDTH + offset) or (bullet.rect.centerx < 0 - offset):
            bullet_sprites.remove(bullet)
            print(f"Delete bullet")
        elif (bullet.rect.centery > SCREEN_HEIGHT + offset) or (bullet.rect.centery < 0 - offset):
            bullet_sprites.remove(bullet)
            print(f"Delete bullet")

#------------------------------------------------------------------------------
# Main loop:
#------------------------------------------------------------------------------

clock = pygame.time.Clock()
spawn_asteroid_time = current_time_ms = pygame.time.get_ticks()
game_loop = True

asteroid_sprites.add(Asteroid(SCREEN_SIZE, screen_radius))

while game_loop:
    # Set the FPS
    dt = clock.tick(FPS) / 1000

    # Process input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
    
    # Get keys status
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] == True:
        spaceship.shoot(bullet_sprites)

    if keys[pygame.K_LEFT] == True:
        spaceship.rotate_left(dt)
    elif keys[pygame.K_RIGHT] == True:
        spaceship.rotate_right(dt)

    current_time_ms = pygame.time.get_ticks()
    if current_time_ms - spawn_asteroid_time >= DELAY_BEFORE_SPAWN_ASTEROID_MS:
        spawn_asteroid_time = current_time_ms
        asteroid_sprites.add(Asteroid(SCREEN_SIZE, screen_radius))
    
    sprites.update(dt)
    bullet_sprites.update(dt)
    asteroid_sprites.update(dt)

    check_bullets_position()

    # pygame.sprite.groupcollide(asteroids, bullets, True, True, pygame.sprite.collide_circle)
    # pygame.sprite.spritecollide(spaceship, asteroids, True, pygame.sprite.collide_circle)
    # pygame.sprite.spritecollide(earth, asteroids, True, pygame.sprite.collide_circle)
    
    screen.fill(BLACK)
    sprites.draw(screen)
    bullet_sprites.draw(screen)
    asteroid_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()