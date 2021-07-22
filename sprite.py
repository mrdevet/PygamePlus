# Copyright 2021 Casey Devet
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

################################################################################
#                              MODULE DESCRIPTION
################################################################################

"""
TODO
"""

################################################################################
#                               GLOBAL VARIABLES
################################################################################

import math
import pygame

from screen import get_active_screen, to_pygame_coordinates

_collision_functions = {
    "rect": pygame.sprite.collide_rect,
    "circle": pygame.sprite.collide_circle,
    "mask": pygame.sprite.collide_mask
}

################################################################################
#                                 SPRITE CLASS
################################################################################

class Sprite (pygame.sprite.Sprite):

    def __init__ (self, image_file=None):
        pygame.sprite.Sprite.__init__(self)
        if image_file is None:
            self._original_image = pygame.Surface((1, 1))
        else:
            self._original_image = pygame.image.load(image_file)
        self._scaled_image = self._original_image
        self.image = self._original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0
        self._pos = pygame.Vector2(0, 0)
        self._dir = 0
        self._move_ratio = pygame.Vector2(1, 0)
        self._scale = pygame.Vector2(1, 1)
        self._dirty_scale = False
        self._smooth_scale = False
        self._rotates = False
        self._tilt = 0
        self._dirty_rotate = False
        self._dirty_mask = True
        self._on_update_func = None
        self._click_funcs = [None for _ in range(5)]
        self._release_funcs = [None for _ in range(5)]
        self._drag_funcs = [None for _ in range(5)]


    ### Visibility Methods

    def show (self):
        active_screen = get_active_screen()
        if active_screen is not None:
            self.add(active_screen)

    def hide (self):
        active_screen = get_active_screen()
        if active_screen is not None:
            self.remove(active_screen)

    def is_visible (self):
        active_screen = get_active_screen()
        return active_screen is not None and self in active_screen


    ### Position Methods

    def set_position (self, x, y=None):
        if y is None:
            self._pos = pygame.Vector2(x)
        else:
            self._pos = pygame.Vector2(x, y)

    def get_position (self):
        return tuple(self._pos)

    def set_x (self, x):
        self.set_position(x, self._pos.y)

    def get_x (self):
        return self._pos.x

    def set_y (self, y):
        self.set_position(self._pos.x, y)

    def get_y (self):
        return self._pos.y


    ### Direction Methods

    def set_direction (self, direction):
        self._dir = direction
        self._dir %= 360
        self._move_ratio = pygame.Vector2(1, 0).rotate(self._dir)
        if self._rotates:
            self._dirty_rotate = True

    def get_direction (self):
        return self._dir

    def turn_left (self, angle):
        self.set_direction(self._dir + angle)

    def turn_right (self, angle):
        self.set_direction(self._dir - angle)


    ### Movement Methods

    def move_forward (self, distance):
        self.set_position(self._pos + distance * self._move_ratio)

    def move_backward (self, distance):
        self.set_position(self._pos - distance * self._move_ratio)

    
    ### Scaling and Rotating Image Methods

    def scale (self, factor, smooth=False):
        self._scale.x = factor
        self._scale.y = factor
        self._dirty_scale = True
        self._dirty_mask = True
        self._smooth_scale = smooth

    def scale_width (self, factor, smooth=False):
        self._scale.x = factor
        self._dirty_scale = True
        self._dirty_mask = True
        self._smooth_scale = smooth

    def scale_height (self, factor, smooth=False):
        self._scale.y = factor
        self._dirty_scale = True
        self._dirty_mask = True
        self._smooth_scale = smooth

    def set_image_rotates (self, rotates=True):
        self._rotates = rotates
        self._dirty_rotate = True
        self._dirty_mask = True

    def get_image_rotates (self):
        return self._rotates

    def set_image_tilt (self, angle):
        self._tilt = angle
        self._tilt %= 360
        self._dirty_rotate = True
        self._dirty_mask = True
    
    def get_image_tilt (self):
        return self._tilt


    ### Update Method

    def _clean_image (self):
        if self._dirty_scale:
            orig_width, orig_height = self._original_image.get_size()
            new_width = round(self._scale.x * orig_width)
            new_height = round(self._scale.y * orig_height)
            if self._smooth_scale:
                self._scaled_image = pygame.transform.smoothscale(
                        self._original_image, (new_width, new_height))
            else:
                self._scaled_image = pygame.transform.scale(
                        self._original_image, (new_width, new_height))
            self._dirty_rotate = True
            self._dirty_scale = False

        if self._dirty_rotate:
            angle = self._dir + self._tilt if self._rotates else self._tilt
            self.image = pygame.transform.rotate(self._scaled_image, angle)
            self._dirty_rotate = False

    def _clean_mask (self):
        if self._dirty_mask:
            self.mask = pygame.mask.from_surface(self.image)
            self._dirty_mask = False

    def update (self, screen=None):
        if self._on_update_func is not None:
            self._on_update_func()
        self._clean_image()
        self.rect = self.image.get_rect()
        if screen is None:
            self.rect.center = to_pygame_coordinates(self._pos)
        else:
            self.rect.center = screen.to_pygame_coordinates(self._pos)


    ### Add Custom Update Function

    def on_update (self, func):
        self._on_update_func = func


    ### Other Sprite Methods

    def get_distance_to (self, other):
        return self._pos.distance_to(other._pos)

    def get_direction_to (self, other):
        return pygame.Vector2(1, 0).angle_to(other._pos - self._pos)


    ### Collision Methods

    def is_touching_point (self, x, y=None, method="rect"):
        # If this sprite isn't visible, then it can't be in collision
        if not self.is_visible():
            return False

        # Get the collision detection function for the given method
        if isinstance(method, str):
            if method not in _collision_functions:
                raise ValueError(f"Invalid collision method: {method}")
            method = _collision_functions[method]

        # Create the other "sprite"
        if y is None:
            x, y = x
        other_sprite = pygame.sprite.Sprite()
        pygame_x, pygame_y = to_pygame_coordinates(x, y)
        other_sprite.rect = pygame.Rect(pygame_x, pygame_y, 1, 1)
        other_sprite.radius = 0.5
        other_sprite.mask = pygame.mask.Mask((1, 1), True)

        # Update the turtle and, if dirty, get its mask
        self._clean_image()
        if method == pygame.sprite.collide_mask:
            self._clean_mask()

        # Collision detection if given a point
        return bool(method(self, other_sprite))

    def get_touching (self, others, method="rect"):
        # If this sprite isn't visible, then it can't be in collision
        if not self.is_visible():
            return False

        # Get the collision detection function for the given method
        if isinstance(method, str):
            if method not in _collision_functions:
                raise ValueError(f"Invalid collision method: {method}")
            method = _collision_functions[method]

        # Update the turtle and, if dirty, get its mask
        self._clean_image()
        if method == pygame.sprite.collide_mask:
            self._clean_mask()

        # If given a list, loop through it use the method from above
        if isinstance(other, list):
            hit_list = []
            for other_sprite in other:
                other_sprite._clean_image()
                if method == pygame.sprite.collide_mask:
                    other_sprite._clean_mask()
                if other in active_screen and bool(method(self, other_sprite)):
                    hit_list.append(other)
            return hit_list
        
        # If given a pygame sprite group, use the pygame function for 
        # collision detection with a group
        elif isinstance(other, pygame.sprite.Group):
            other.update()
            hit_list = pygame.sprite.spritecollide(self, other, False, method)
            return hit_list

        # If given an invalid argument, just return False
        else:
            return ValueError("Invalid argument!")

    def is_touching (self, other, method="rect"):
        # If this sprite isn't visible, then it can't be in collision
        if not self.is_visible():
            return False

        active_screen = get_active_screen()

        # Get the collision detection function for the given method
        if isinstance(method, str):
            if method not in _collision_functions:
                raise ValueError(f"Invalid collision method: {method}")
            method = _collision_functions[method]

        # Update the turtle and, if dirty, get its mask
        self._clean_image()
        if method == pygame.sprite.collide_mask:
            self._clean_mask()

        # If given just a sprite, put it into a list
        if isinstance(other, pygame.sprite.Sprite):
            other._clean_image()
            if method == pygame.sprite.collide_mask:
                other._clean_mask()
            return other in active_screen and bool(method(self, other))

        # If given a list, loop through it use the method from above
        elif isinstance(other, list):
            for other_sprite in other:
                other_sprite._clean_image()
                if method == pygame.sprite.collide_mask:
                    other_sprite._clean_mask()
                if other in active_screen and bool(method(self, other_sprite)):
                    return True
            return False
        
        # If given a pygame sprite group, use the pygame function for 
        # collision detection with a group
        elif isinstance(other, pygame.sprite.Group):
            other.update()
            hit_list = pygame.sprite.spritecollide(self, other, False, method)
            return len(hit_list) > 0

        # If given an invalid argument, just return False
        else:
            return ValueError("Invalid argument!")


    ### Click Event Methods

    def on_click (self, func, button=1):
        # TODO: Add ability to only have click events when mask clicked on.
        #   This could make use of the is_touching_point() method
        if 1 <= button <= 5:
            self._click_funcs[button - 1] = func
        else:
            raise ValueError("Invalid button!")

    def on_release (self, func, button=1):
        if 1 <= button <= 5:
            self._release_funcs[button - 1] = func
        else:
            raise ValueError("Invalid button!")

    def on_drag (self, func, button=1):
        if 1 <= button <= 5:
            self._drag_funcs[button - 1] = func
        else:
            raise ValueError("Invalid button!")

        

__all__ = [
    "Sprite"
]
