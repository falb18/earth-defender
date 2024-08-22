import pygame
import math
import random
from constants import *

BULLET_SPEED = 2.5
SPACESHIP_IMG_SIZE = (20, 20)
EARTH_IMG_SIZE = (150, 150)
EARTH_RADIUS = 75
ASTEROID_SPEED = 0.2
ASTEROID_ROTATION_DELAY = 50 # milliseconds

SHOOT_DELAY = 150 / 1000 # milliseconds

class Bullet(pygame.sprite.Sprite):
    def __init__(self, spaceship_center, direction_vector):
        # The direction vector corresponds to the angle of the spaceship, so the bullet
        # moves on the same direction.
        super().__init__()
        self.image = pygame.Surface((5,5))
        self.rect = self.image.get_rect()
        # The radius mathes the sprite collision circle
        self.radius = int(self.rect.width/2)
        pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius, 1)
        
        self.rect.center = spaceship_center
        self.vector = pygame.math.Vector2(direction_vector)
    
    def update(self, delta_time):
        self.rect.center += self.vector * (BULLET_SPEED * delta_time)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        super().__init__()
        self.pivot = pygame.math.Vector2(init_pos)
        # Create a surface and draw a triangle on top of it
        self.spaceship_img = pygame.Surface(SPACESHIP_IMG_SIZE, pygame.SRCALPHA)
        # Define the points for the triangle
        points = [[0,0],[0,20],[20,10]]
        pygame.draw.polygon(self.spaceship_img, YELLOW, points)
        self.image = self.spaceship_img.copy()
        self.rect = self.image.get_rect()
        # Define radius for sprite collision circle
        self.radius = int(self.rect.width/2)

        # Define the offset coordinates where the spaceship is going to be placed
        self.radius_offset = 100
        self.offset_vector = pygame.math.Vector2(self.radius_offset, 0)
        self.rect.center = self.pivot + self.offset_vector

        self.angular_velocity = 80
        self.angle_rotation = 0
        
        self.shooting_enabled = True
        self.shoot_time = 0

        self.health = 100

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
            bullets.add(Bullet(self.rect.center, self.offset_vector))
            self.shooting_enabled = False

class Earth(pygame.sprite.Sprite):
    def __init__(self, init_pos):
        super().__init__()
        self.earth_img = pygame.Surface(EARTH_IMG_SIZE, pygame.SRCALPHA)
        pygame.draw.circle(self.earth_img, CYAN, [75,75], EARTH_RADIUS)
        self.image = self.earth_img.copy()
        self.rect = self.image.get_rect()
        # The radius matches the sprite collision circle
        self.radius = int(self.rect.width/2)
        self.rect.center = init_pos

        self.health = 100
    
    def update(self, delta_time):
        pass

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen_size, screen_radius):
        super().__init__()
        screen_width = screen_size[0]
        screen_height = screen_size[1]
        # Set a random size for the asteroid
        img_size = random.randint(15,35)
        img_center = [img_size/2,img_size/2]
        self.asteroid_img = pygame.Surface([img_size,img_size], pygame.SRCALPHA)
        
        # Calculate the points for the polygon
        points = []
        sides = 8
        poly_angle = 360/sides # Get the angle from the center of the polygon
        for i in range(0,sides):
            angle_radian = math.radians(poly_angle*i-(poly_angle/2))
            x = img_center[0]+(img_size/2)*math.cos(angle_radian)
            y = img_center[1]+(img_size/2)*math.sin(angle_radian)
            points.append([x,y])
        pygame.draw.polygon(self.asteroid_img, WHITE, points)
        
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