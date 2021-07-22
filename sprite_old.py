
import math
import pygame
from pygame.locals import *

collision_functions = {
    "rect": pygame.sprite.collide_rect,
    "circle": pygame.sprite.collide_circle,
    "mask": pygame.sprite.collide_mask
}

all_sprites = pygame.sprite.Group()

class Sprite (pygame.sprite.Sprite):
    # What has to be passed when you create a sprite.
    #   image_file: The filename of the image.
    #   name: The name you want to call the Sprite for id purposes.
    #   lacation: The (x,y) initial location of where to draw the image.
    def __init__ (self, image_file, location=None):
        pygame.sprite.Sprite.__init__(self) # Call Sprite initializer
        self.image = pygame.image.load(image_file)
        self._image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left = 0 if location is None else location[0]
        self.rect.top = 0 if location is None else location[1]
        self.x_speed = 0 # The default x_speed
        self.y_speed = 0 # The default y_speed
        self.speed = 0
        self.direction = 0
        self.last_position = location
        all_sprites.add(self)

    # Moves the sprite in the direction it's facing at the current speed it's set for.
    def update (self):
        self.last_position = self.rect.x, self.rect.y
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def undo_update (self):
        self.rect.x, self.rect.y = self.last_position

    # Sets the x position of the Sprite.
    def set_x (self, x):
        self.rect.x = x

    # Returns the current x location of the Sprite.
    def get_x (self):
        return self.rect.x

    # Sets the y position of the Sprite.
    def set_y (self, y):
        self.rect.y = y

    # Returns the current y location of the Sprite.
    def get_y (self):
        return self.rect.y

    def go_to (self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_position (self):
        return self.rect.x, self.rect.y

    # Sets the speed of the Sprite.
    def set_speed (self, speed):
        self.speed = speed
        self.calc_xy_speeds()

    def get_speed (self):
        return self.speed

    def set_direction (self, direction):
        self.direction = direction % 360
        self.calc_xy_speeds()

    def get_direction (self):
        return self.direction

    def turn (self, angle):
        self.direction = self.direction + angle
        self.calc_xy_speeds()

        # Store the current center so that we can use it to set the center of the new rotated image.
        old_center_x = self.rect.centerx
        old_center_y = self.rect.centery

        # Rotate the original image.
        self.image = pygame.transform.rotate(self._image, self.direction)

        # Update the sprites rect with the new width and height after the rotate.
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height

        # Change the center of the new rotated image to be the same center as the old image
        self.rect.centerx = old_center_x
        self.rect.centery = old_center_y

    def set_direction_towards (self, x, y):
        delta_x = x - self.rect.x
        delta_y = y - self.rect.y
        direction = round(math.degrees(math.atan2(delta_y, delta_x)), 12)
        self.set_direction(direction)

    # Calculate the x and y speeds based on the current angle.
    def calc_xy_speeds(self):
        angleRadians = -math.radians(self.direction)
        self.x_speed = round(self.speed * math.cos(angleRadians), 12)
        self.y_speed = round(self.speed * math.sin(angleRadians), 12)

    def set_x_speed (self, new_x_speed):
        self.x_speed = new_x_speed
        self.direction = math.degrees(math.atan2(-self.y_speed,self.x_speed)) % 360

    def set_y_speed (self, new_y_speed):
        self.y_speed = new_y_speed
        self.direction = math.degrees(math.atan2(-self.y_speed,self.x_speed)) % 360

    def get_x_speed (self):
        return self.x_speed

    def get_y_speed (self):
        return self.y_speed

    def is_off_right_edge (self, screen):
        return self.rect.x + self.rect.width > screen.get_width()

    def is_off_left_edge (self, screen):
        return self.rect.x < 0

    def is_off_bottom_edge (self, screen):
        return self.rect.y + self.rect.height > screen.get_height()

    def is_off_top_edge (self, screen):
        return self.rect.y < 0

    def is_touching (self, other, remove_sprite=False, method="rect"):
        if isinstance(method, str):
            if method not in collision_functions:
                raise ValueError(f"Invalid collision method: {method}")
            method = collision_functions[method]
        if isinstance(other, pygame.sprite.Sprite):
            if other.alive() and bool(method(self, other)):
                if remove_sprite:
                    other.kill()
                return True
            return False
        elif isinstance(other, pygame.sprite.Group):
            hit_list = pygame.sprite.spritecollide(self, other, remove_sprite, method)
            return len(hit_list) > 0
        else:
            return False


def get_all_sprites ():
    return all_sprites


def update_all_sprites ():
    all_sprites.update()


def draw_all_sprites (screen):
    all_sprites.draw(screen)


def kill_all_sprites ():
    for sprite in all_sprites.sprites():
        sprite.kill()
        

__all__ = ["Sprite", "get_all_sprites", "update_all_sprites", "draw_all_sprites", "kill_all_sprites"]
