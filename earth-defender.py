import pygame
from constants import *
from pygame import sprite
import math
import random

# Window settings
WIDTH = 640 # game window width
HEIGHT = 480 # game window height
FPS = 60 # frames per second

# Define player (spaceship)
class Spaceship(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = WIDTH/2
        self.y = HEIGHT/2 
        self.image_orig = spaceship_img
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # Define radius for sprite collision circle
        self.radius = int(self.rect.width/2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)

        # Define the offset where the space will be positioned
        self.radius_offset = 100
        self.vector = pygame.math.Vector2(self.radius_offset, 0)
        self.rect.center = [self.x + self.vector.x, self.y + self.vector.y]

        # Define spaceship velocity
        self.angular_velocity = 2
        self.angle = 0
        
        self.last_update = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250

    def update(self):
        self.check_keystate()
        self.circular_motion()
    
    # Do the math for rotation when key is pressed
    def check_keystate(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.angle = (self.angle - self.angular_velocity) % 360
        elif keystate[pygame.K_RIGHT]:
            self.angle = (self.angle + self.angular_velocity) % 360
        
        radians = math.radians(self.angle)
        self.vector.x = int(self.radius_offset * math.cos(radians))
        self.vector.y = int(self.radius_offset * math.sin(radians))
        
        if keystate[pygame.K_SPACE]:
            self.shoot()
    
    # Rotate the image
    def circular_motion(self):         
        current_update = pygame.time.get_ticks()
        if current_update - self.last_update > 1:
            self.last_update = current_update
            # The angle has to be negative to follow the vector circular motion
            new_image = pygame.transform.rotate(self.image_orig, -self.angle)
            previous_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)
            self.rect.centerx = self.x + self.vector.x
            self.rect.centery = self.y + self.vector.y
    
    # Spawn bullets while the space bar is hold down
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            bullet = Bullet(self.rect.center, self.vector)
            bullets.add(bullet)

class Bullet(sprite.Sprite):
    # It's important to get the player's vector since the bullet
    # has to move on the same direction.
    def __init__(self, player_center, player_vector):
        super().__init__()
        self.image = pygame.Surface((5,5))
        self.rect = self.image.get_rect()
        # The radius mathes the sprite collision circle
        self.radius = int(self.rect.width/2)
        pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius, 1)
        self.rect.center = player_center
        self.vector = pygame.math.Vector2(player_vector)
        self.pos = self.rect.center
    
    def update(self):
        self.pos += self.vector * 0.04
        self.rect.center = self.pos
        # If bullet is off the screen delete it
        if self.rect.centerx > WIDTH or self.rect.centery > HEIGHT or \
                self.rect.centerx < 0 or self.rect.centery < 0:
            self.kill()

class Earth(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = earth_img
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # The radius mathes the sprite collision circle
        self.radius = int(self.rect.width/2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)
        self.rect.center = [WIDTH/2, HEIGHT/2]
    
    def update(self):
        pass

class Asteroid(sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Define random size
        img_size = random.randint(15,35)
        img_center = [img_size/2,img_size/2]
        self.img_orig = pygame.Surface([img_size,img_size], pygame.SRCALPHA)
        
        # Get the points for the polygon
        points = []
        sides = 8
        poly_angle = 360/sides # Get the angle from the center of the polygon
        for i in range(0,sides):
            angle_radian = math.radians(poly_angle*i-(poly_angle/2))
            x = img_center[0]+(img_size/2)*math.cos(angle_radian)
            y = img_center[1]+(img_size/2)*math.sin(angle_radian)
            points.append([x,y])
        pygame.draw.polygon(self.img_orig, WHITE, points)
        
        self.image = self.img_orig.copy()
        self.rect = self.image.get_rect()
        # Define radius for sprite collision circle
        self.radius = int(self.rect.width*0.9/2)
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)

        # Define random initial position:
        # Set a random angle and sum the offset so the asteroid spawns off the screen
        self.angular_velocity = 3
        self.asteroid_angle = random.randint(0,360)
        asteroid_angle_rad = math.radians(self.asteroid_angle)
        x = WIDTH/2 - int(screen_radius * math.cos(asteroid_angle_rad))
        y = HEIGHT/2 - int(screen_radius * math.sin(asteroid_angle_rad))
        
        # Limit the vector distance within the screen size
        if x < 0:
            x = 0
        elif x > WIDTH:
            x = WIDTH
        if y < 0:
            y = 0
        elif y > HEIGHT:
            y = HEIGHT
        
        # Vector between the center of the earth and the initial position of the asteroid
        self.rect.center = [x,y]
        self.vector = pygame.math.Vector2([self.rect.centerx - WIDTH/2, self.rect.centery - HEIGHT/2])
        self.pos = self.rect.center

        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.pos -= self.vector * 0.0025
        self.rect.center = self.pos

    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > 50:
            self.last_update = current_time
            self.asteroid_angle = (self.asteroid_angle + self.angular_velocity) % 360
            new_image = pygame.transform.rotate(self.img_orig, self.asteroid_angle)
            previous_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)
            self.rect.center = previous_center

#------------------------------------------------------------------------------
# Main loop:
#------------------------------------------------------------------------------

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_radius = math.sqrt(WIDTH**2 + HEIGHT**2)/2
pygame.display.set_caption("Earth Defender")

# Load images
img_size = [20, 20]
# Create a surface and then draw a triangle on top of it
spaceship_img = pygame.Surface(img_size, pygame.SRCALPHA)
# Define the point to draw the triangle
points = [[0,0],[0,20],[20,10]]
pygame.draw.polygon(spaceship_img, YELLOW, points)

img_size = [150,150]
earth_radius = 75
earth_img = pygame.Surface(img_size, pygame.SRCALPHA)
pygame.draw.circle(earth_img, CYAN, [75,75], earth_radius)

# Create game characters
spaceship = Spaceship()
earth = Earth()
asteroid = Asteroid()

# Create sprite group
sprites = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
sprites.add(spaceship)
sprites.add(earth)
asteroids.add(asteroid)

clock = pygame.time.Clock()
spawn_asteroid_time = pygame.time.get_ticks()
main_loop = True

while main_loop:
    # Set the FPS
    clock.tick(FPS)

    # Process input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_loop = False
    
    if pygame.time.get_ticks() - spawn_asteroid_time > 3000:
        spawn_asteroid_time = pygame.time.get_ticks()
        asteroid = Asteroid()
        asteroids.add(asteroid)
    
    # Update each sprite in the group
    sprites.update()
    bullets.update()
    asteroids.update()

    sprite.groupcollide(asteroids, bullets, True, True, sprite.collide_circle)
    sprite.spritecollide(spaceship, asteroids, True, sprite.collide_circle)
    sprite.spritecollide(earth, asteroids, True, sprite.collide_circle)
    
    # Draw / render sprites on the main screen
    screen.fill(BLACK)
    sprites.draw(screen)
    bullets.draw(screen)
    asteroids.draw(screen)

    # Finally show eveything on the screen
    pygame.display.flip()

pygame.quit()