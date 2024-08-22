import pygame
import math
from os import path

from constants import *
from objects import *

DELAY_BEFORE_SPAWN_ASTEROID_MS = 3000

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
FPS = 60 # frames per second

#------------------------------------------------------------------------------
# Variables:
#------------------------------------------------------------------------------

resources_dir = "res"

#------------------------------------------------------------------------------
# Game init:
#------------------------------------------------------------------------------

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_radius = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2)/2
pygame.display.set_caption("Earth Defender")

# Load images
background_img = pygame.image.load(path.join(resources_dir, "starfield-background.png"))
background_img = background_img.convert_alpha()
background_rect = background_img.get_rect()

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
        elif (bullet.rect.centery > SCREEN_HEIGHT + offset) or (bullet.rect.centery < 0 - offset):
            bullet_sprites.remove(bullet)

def check_collision_asteroids():
    asteroids = pygame.sprite.spritecollide(spaceship, asteroid_sprites, True, pygame.sprite.collide_circle)
    for asteroid in asteroids:
        spaceship.health -= asteroid.radius * 0.5
        print(f"Spaceship health: {spaceship.health}")
        if spaceship.health <= 0:
            print("Spaceship destroyed")
            spaceship.health = 100

#------------------------------------------------------------------------------
# Main loop:
#------------------------------------------------------------------------------

print("Game controls:")
print("p: pause")

clock = pygame.time.Clock()
spawn_asteroid_time = current_time_ms = pygame.time.get_ticks()
game_loop = True
game_pause = False

asteroid_sprites.add(Asteroid(SCREEN_SIZE, screen_radius))

while game_loop:
    # Set the FPS
    dt = clock.tick(FPS) / 1000

    # Process input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_pause = not game_pause
    
    if not game_pause:

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

        # Check the collision of the objects. In some cases we have to delete the sprite if a collision happens
        sprites_collide = pygame.sprite.groupcollide(asteroid_sprites, bullet_sprites, True, True, pygame.sprite.collide_circle)
        check_collision_asteroids()
        pygame.sprite.spritecollide(earth, asteroid_sprites, True, pygame.sprite.collide_circle)
    
    screen.fill(BLACK)
    screen.blit(background_img, background_rect)
    sprites.draw(screen)
    bullet_sprites.draw(screen)
    asteroid_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()