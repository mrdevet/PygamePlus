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

import pygame

class Screen (pygame.sprite.Group):

    _active = None

    def __init__ (self, width, height, title=""):
        pygame.sprite.Group.__init__(self)
        self._surface = None
        self._width = width
        self._height = height
        self._title = title
        self._color = "white"
        self._image = None
        self._image_name = None
        self._key_press_funcs = {}
        self._key_release_funcs = {}
        self._key_hold_funcs = {}
        self._click_funcs = [None for _ in range(5)]
        self._canvas = pygame.Surface((width, height), pygame.SRCALPHA)



    def open (self):
        if Screen._active is not None and Screen._active != self:
            self._active._close()
        self._surface = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(self._title)
        Screen._active = self

    def _close (self):
        pass

    def is_open (self):
        return self == Screen._active



    def set_size (self, width, height):
        self._width = width
        self._height = height
        if self.is_open():
            self._surface = pygame.display.set_mode((self._width, self._height))
            self.update()
        old_canvas = self._canvas
        self._canvas = pygame.Surface((width, height), pygame.SRCALPHA)

    def get_size (self):
        return self._width, self._height

    def set_width (self, width):
        self.set_size(width, self._height)

    def get_width (self):
        return self._width

    def set_height (self, height):
        self.set_size(self._width, height)

    def get_height (self):
        return self._height

    def set_title (self, title):
        self._title = title

    def get_title (self):
        return self._title



    def set_background_color (self, color):
        self._color = color

    def get_background_color (self, color):
        return self._color

    def set_background_image (self, image):
        if image is None:
            self._image = None
            self._image_name = None
        else:
            self._image = pygame.image.load(image)
            self._image_name = image

    def get_background_image (self, image):
        return self._image_name


    
    def get_canvas (self):
        return self._canvas

    def clear_canvas (self):
        self._canvas.fill(0)

    def clear_rect (self, remove_sprites=False):
        pass

    def clear_circle (self, remove_sprites=False):
        pass



    def clear (self):
        self._color = "white"
        self._image = None
        self._image_name = None
        self._canvas.fill(0)
        self.empty()

    def update (self):
        self._surface.fill(self._color)
        if self._image is not None:
            rect = self._image.get_rect()
            rect.centerx = self._width / 2
            rect.centery = self._height / 2
            self._surface.blit(self._image, rect)
        pygame.sprite.Group.update(self, self)
        self._surface.blit(self._canvas, (0, 0))
        pygame.sprite.Group.draw(self, self._surface)
        pygame.display.flip()



    def on_key_press (self, func, key=None):
        if key is None:
            self._key_press_funcs[None] = func
        elif isinstance(key, str):
            self._key_press_funcs[pygame.key.key_code(key)] = func
        else:
            self._key_press_funcs[key] = func

    def on_key_release (self, func, key=None):
        if key is None:
            self._key_release_funcs[None] = func
        elif isinstance(key, str):
            self._key_release_funcs[pygame.key.key_code(key)] = func
        else:
            self._key_release_funcs[key] = func
    
    def on_key_hold (self, func, key=None):
        if key is None:
            self._key_hold_funcs[None] = func
        elif isinstance(key, str):
            self._key_hold_funcs[pygame.key.key_code(key)] = func
        else:
            self._key_hold_funcs[key] = func

    def on_click (self, func, button=1):
        if 1 <= button <= 5:
            self._click_funcs[button - 1] = func
        else:
            raise ValueError("Invalid button!")



    def to_pygame_coordinates (self, x, y=None):
        if y is None:
            x, y = x
        pygame_x = x + self._width / 2
        pygame_y = self._height / 2 - y
        return pygame.Vector2(pygame_x, pygame_y)

    def from_pygame_coordinates (self, pygame_x, pygame_y=None):
        if pygame_y is None:
            pygame_x, pygame_y = pygame_x
        x = pygame_x - self._width / 2
        y = self._height / 2 - pygame_y
        return x, y



def get_active_screen ():
    return Screen._active


def to_pygame_coordinates (x, y=None):
    if Screen._active is None:
        raise RuntimeError("No screen is active!")
    return Screen._active.to_pygame_coordinates(x, y)


def from_pygame_coordinates (pygame_x, pygame_y=None):
    if Screen._active is None:
        raise RuntimeError("No screen is active!")
    return Screen._active.from_pygame_coordinates(pygame_x, pygame_y)
    

__all__ = [
    "Screen", 
    "get_active_screen", 
    "to_pygame_coordinates", 
    "from_pygame_coordinates"
]
