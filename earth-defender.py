import pygame
import math

from constants import *
from objects import *

# Window settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
FPS = 60 # frames per second

#------------------------------------------------------------------------------
# Main loop:
#------------------------------------------------------------------------------

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_radius = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2)/2
pygame.display.set_caption("Earth Defender")

# Create game characters
spaceship = Spaceship(SCREEN_CENTER)
earth = Earth(SCREEN_CENTER)
asteroid = Asteroid(SCREEN_CENTER, screen_radius)

# Create sprite group
sprites = pygame.sprite.Group()
# bullets = pygame.sprite.Group()
# asteroids = pygame.sprite.Group()

sprites.add(spaceship, earth)
# asteroids.add(asteroid)

clock = pygame.time.Clock()
spawn_asteroid_time = pygame.time.get_ticks()
game_loop = True

while game_loop:
    # Set the FPS
    clock.tick(FPS)

    # Process input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
    
    # if pygame.time.get_ticks() - spawn_asteroid_time > 3000:
    #     spawn_asteroid_time = pygame.time.get_ticks()
    #     asteroid = Asteroid()
    #     asteroids.add(asteroid)
    
    # Update each sprite in the group
    sprites.update()
    # bullets.update()
    # asteroids.update()

    # pygame.sprite.groupcollide(asteroids, bullets, True, True, pygame.sprite.collide_circle)
    # pygame.sprite.spritecollide(spaceship, asteroids, True, pygame.sprite.collide_circle)
    # pygame.sprite.spritecollide(earth, asteroids, True, pygame.sprite.collide_circle)
    
    # Draw / render sprites on the main screen
    screen.fill(BLACK)
    sprites.draw(screen)
    # bullets.draw(screen)
    # asteroids.draw(screen)

    # Finally show eveything on the screen
    pygame.display.flip()

pygame.quit()