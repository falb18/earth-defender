import pygame
import math
import random
from os import path

from constants import *

BULLET_SPEED = 2.5

SPACESHIP_FACE_EAST = -90

EARTH_DIAMETER = 100 # This is the actual radius of the planet on the image

ASTEROID_SPEED = 0.2
ASTEROID_ROTATION_DELAY = 50 # milliseconds
ASTEROIDS_IMG_FILES_LIST = ["meteorBrown_tiny1.png", "meteorBrown_small1.png",
                            "meteorBrown_med1.png", "meteorBrown_big3.png"]

SHOOT_DELAY = 150 / 1000 # milliseconds

#------------------------------------------------------------------------------
# Variables:
#------------------------------------------------------------------------------

asteroids_imgs = []

#------------------------------------------------------------------------------
# Objects:
#------------------------------------------------------------------------------

class Bullet(pygame.sprite.Sprite):
    def __init__(self, spaceship_center, direction_vector, angle_rotation):
        # The direction vector corresponds to the angle of the spaceship, so the bullet
        # moves on the same direction.
        super().__init__()
        # self.image = pygame.Surface((5,5))
        self.image = pygame.image.load(path.join(RESOURCES_DIR, "laserGreen11.png"))
        self.image = self.image.convert_alpha()
        self.image = pygame.transform.rotate(self.image, SPACESHIP_FACE_EAST - angle_rotation)
        self.rect = self.image.get_rect()
        # The radius mathes the sprite collision circle
        self.radius = int(self.rect.width/2)
        
        self.rect.center = spaceship_center
        self.vector = pygame.math.Vector2(direction_vector)
    
    def update(self, delta_time):
        self.rect.center += self.vector * (BULLET_SPEED * delta_time)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        super().__init__()
        self.pivot = pygame.math.Vector2(init_pos)
        self.spaceship_img = pygame.image.load(path.join(RESOURCES_DIR, "playerShip3_green.png"))
        self.spaceship_img = self.spaceship_img.convert_alpha()
        self.spaceship_img = pygame.transform.rotate(self.spaceship_img, SPACESHIP_FACE_EAST)
        self.image = self.spaceship_img.copy()
        self.rect = self.image.get_rect()
        # Define radius for sprite collision circle
        self.radius = int(self.rect.width/2)

        # Define the offset coordinates where the spaceship is going to be placed
        # The way the radius offset is defined is arbitrary
        self.radius_offset = (EARTH_DIAMETER/2) + (self.rect.width * 0.75)
        self.offset_vector = pygame.math.Vector2(self.radius_offset, 0)
        self.rect.center = self.pivot + self.offset_vector

        self.angular_velocity = 80
        self.angle_rotation = 0
        
        self.shooting_enabled = True
        self.shoot_time = 0

        self.health = 100
        self.lives = 3

    def update(self, delta_time):
        # Rotate the position of the spaceship. To get the new position calculate each
        # component of the vector
        radians = math.radians(self.angle_rotation)
        self.offset_vector.x = int(self.radius_offset * math.cos(radians))
        self.offset_vector.y = int(self.radius_offset * math.sin(radians))
        self.rotate_image()

        if self.shooting_enabled == False:
            self.shoot_time += delta_time
            if self.shoot_time >= SHOOT_DELAY:
                self.shooting_enabled = True
                self.shoot_time = 0
    
    def rotate_left(self, delta_time):
        self.angle_rotation -= self.angular_velocity * delta_time
        self.angle_rotation %= 360

    def rotate_right(self, delta_time):
        self.angle_rotation += self.angular_velocity * delta_time
        self.angle_rotation %= 360
    
    def rotate_image(self):
        # The angle has to be negative to follow the circular motion of the offset vector
        self.image = pygame.transform.rotate(self.spaceship_img, -self.angle_rotation)
        self.rect = self.image.get_rect(center = self.pivot + self.offset_vector)
    
    def shoot(self, bullets):
        """ The function adds a new Bullet sprite to the group bullet_sprites """
        if self.shooting_enabled == True:
            bullets.add(Bullet(self.rect.center, self.offset_vector, self.angle_rotation))
            self.shooting_enabled = False

class Earth(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        super().__init__()
        self.earth_img = pygame.image.load(path.join(RESOURCES_DIR, "planet03.png"))
        self.earth_img = self.earth_img.convert_alpha()
        self.image = self.earth_img.copy()
        self.rect = self.image.get_rect()
        # The radius matches the sprite collision circle
        self.radius = EARTH_DIAMETER / 2
        self.rect.center = init_pos

        self.health = 100
    
    def update(self, delta_time):
        pass

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_size, screen_radius):
        super().__init__()
        screen_width = screen_size[0]
        screen_height = screen_size[1]

        self.asteroid_img = random.choice(asteroids_imgs)
        self.image = self.asteroid_img.copy()
        self.rect = self.image.get_rect()
        # Define radius for sprite collision circle
        radius_scale = 0.9
        self.radius = int((self.rect.width*radius_scale)/2)

        # Set a random initial position with a random angle. Sum an offset to the initial
        # postion so the asteroid spawns at the edge of the screen
        self.angular_velocity = 120
        self.asteroid_angle = random.randint(0,360)
        asteroid_angle_rad = math.radians(self.asteroid_angle)
        x = screen_width/2 - int(screen_radius * math.cos(asteroid_angle_rad))
        y = screen_height/2 - int(screen_radius * math.sin(asteroid_angle_rad))
        
        # Limit the position of the asteroid when spawning. It shouldn't be that far from
        # the edge of the screen
        if x < 0:
            x = 0
        elif x > screen_width:
            x = screen_width
        if y < 0:
            y = 0
        elif y > screen_height:
            y = screen_height
        
        # Get the vector between the center of the earth (screen) and the center of the asteroid
        self.rect.center = [x,y]
        self.vector = pygame.math.Vector2([self.rect.centerx - screen_width/2, self.rect.centery - screen_height/2])
        self.pos = self.rect.center

        self.last_update = pygame.time.get_ticks()

    def update(self, delta_time):
        current_time_ms = pygame.time.get_ticks()
        if current_time_ms - self.last_update >= ASTEROID_ROTATION_DELAY:
            self.last_update = current_time_ms
            self.rotate_image(delta_time)
        
        self.pos -= self.vector * (ASTEROID_SPEED * delta_time)
        self.rect.center = self.pos

    def rotate_image(self, delta_time):
        self.asteroid_angle += self.angular_velocity * delta_time
        self.asteroid_angle %= 360
        self.image = pygame.transform.rotate(self.asteroid_img, self.asteroid_angle)
        # Set the previous center of image's rect to keep the same position
        self.rect = self.image.get_rect(center=self.rect.center)

#------------------------------------------------------------------------------
# Auxiliary functions:
#------------------------------------------------------------------------------

def setup_game_objects():
    # Create the images for the different sizes of asteroids
    for asteroid_img_file in ASTEROIDS_IMG_FILES_LIST:
        asteroids_imgs.append(pygame.image.load(path.join(RESOURCES_DIR, asteroid_img_file)).convert_alpha())