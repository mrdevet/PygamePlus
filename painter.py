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
from pygame import Color

from screen import get_active_screen, to_pygame_coordinates
from sprite import *

################################################################################
#                                 SPRITE CLASS
################################################################################

class Painter (Sprite):

    def __init__ (self, image_file=None):
        Sprite.__init__(self, image_file)
        self._pendown = True
        self._pencolor = "black"
        self._pencolor_obj = pygame.Color("black")
        self._pensize = 1
        self._stepsize = 0.1
        self._filling = False
        self._fill_as_moving = None
        self._fillpoly = None
        self._fillcolor = "black"
        self._fillcolor_obj = pygame.Color("black")
        self._surface_over_fill = None

    # Set and get colors

    def set_color (self, color):
        self._pencolor_obj = Color(color)
        self._pencolor = color
        self._fillcolor_obj = Color(color)
        self._fillcolor = color

    def get_colors (self):
        return self._pencolor, self._fillcolor

    def set_pen_color (self, color):
        self._pencolor_obj = Color(color)
        self._pencolor = color

    def get_pen_color (self):
        return self._pencolor

    def set_fill_color (self, color):
        self._fillcolor_obj = Color(color)
        self._fillcolor = color
    
    def get_fill_color (self):
        return self._fillcolor

    def set_pen_width (self, width):
        self._pensize = width

    def get_pen_width (self):
        return self._pensize

    def set_step_size (self, distance):
        self._stepsize = distance

    def get_step_size (self, distance):
        return self._stepsize

    def put_pen_down (self):
        self._pendown = True

    def pick_pen_up (self):
        self._pendown = False

    def is_pen_down (self):
        return self._pendown

    # Draw on movement

    def _draw_line (self, start, end, canvas=None):
        if canvas is None:
            # Get the active screen's canvas
            screen = get_active_screen()
            if screen is None:
                return
            canvas = screen.get_canvas()

        # Convert to pygame coordinates
        start = to_pygame_coordinates(start)
        end = to_pygame_coordinates(end)

        # If width is 1, use the pygame function
        if self._pensize == 1:
            pygame.draw.line(canvas, self._pencolor_obj, start, end)

        # Otherwise use dots instead
        else:
            # Find geometric properties of the line
            delta = end - start
            distance, direction = delta.as_polar()

            # Draw dots every 0.1 pixels along the line between the points
            radius = self._pensize / 2
            current = start
            delta = pygame.Vector2(self._stepsize, 0).rotate(direction)
            for _ in range(int(distance / self._stepsize)):
                pygame.draw.circle(canvas, self._pencolor_obj, current, radius)
                current += delta
            pygame.draw.circle(canvas, self._pencolor_obj, current, radius)

    def set_position (self, x, y=None):
        if y is None:
            x, y = x

        # Actually move the sprite
        start = self._pos
        Sprite.set_position(self, x, y)            

        # If the turtle is currently creating a filled shape, store
        # the point.
        if self._filling:
            self._fillpoly.append(self._pos)
            self._draw_line(start, self._pos, self._lines_over_fill)

        # Draw the line
        if self._pendown:
            self._draw_line(start, self._pos)

    def walk_path (self, path):
        for point in path:
            self.set_position(point)

    ### Creating Filled Shapes

    def begin_fill (self, as_moving=False):
        self._filling = True
        self._fillpoly = [self._pos]
        self._fill_as_moving = bool(as_moving)
        screen = get_active_screen()
        self._lines_over_fill = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    def end_fill (self):
        '''
        Complete drawing a filled shape.

        This function must be preceded by a call to begin_fill().  When
        this method is called, a filled shape will be drawn using all of the
        points visited since begin_fill() was called.
        '''

        if not self._filling:
            return

        screen = get_active_screen()
        if screen is not None:
            # Get the canvas to draw on
            canvas = screen.get_canvas()

            # Draw the points to the canvas
            points = [to_pygame_coordinates(p) for p in self._fillpoly]
            pygame.draw.polygon(canvas, self._fillcolor, points)

            # Draw the lines back on top of the canvas
            canvas.blit(self._lines_over_fill, (0, 0))
        
        # Reset the filling attributes
        self._filling = False
        self._fillpoly = None
        self._fill_as_moving = None
        self._lines_over_fill = None

    def is_filling (self):
        return self._filling


        

__all__ = [
    "Painter",
    "Color"
]
