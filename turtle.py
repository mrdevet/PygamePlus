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
#                               GLOBAL VARIABLES
################################################################################

import math
import pygame

from painter import Painter
from screen import get_active_screen

################################################################################
#                                 TURTLE CLASS
################################################################################

class Turtle (Painter):
    '''
    A Turtle is a special sprite that can move around the screen and make 
    drawings.  The turtle's movements will be animated so that you can see it's
    movements.

    A turtle object includes all of the movement methods of a Sprite and the
    drawing methods of a Painter.
    '''

    def __init__ (self):
        '''
        Create a Turtle object.
        '''

        Painter.__init__(self, "turtle")

        # The attributes used to animate the turtle
        self.clock = pygame.time.Clock()
        self._frame_rate = 30
        self._speed = 120
        self._step_size = 4
        self._animate = True

        # Set that the turtle image should rotate when the turtle turns
        self.set_image_rotates()

        # Attributes that allow the speed to be maintained over multiple calls 
        # to set_position()
        self._pixels_remaining = 4
        self._redraw_on_part_step = True


    def add (self, *groups):
        '''
        Add this Turtle to the groups.

        When a turtle is added to the active screen, it immediately appears 
        without redrawing the screen.
        '''

        Painter.add(self, *groups)

        # If one of the groups is the active screen, then redraw it so that 
        # the turtle appears immediately.
        active_screen = get_active_screen()
        for group in groups:
            if group == active_screen:
                active_screen.redraw()


    def set_position (self, x, y=None):
        '''
        Move the Turtle to the given coordinates.

        If the sprite is currently drawing a line or fill, movement will cause
        drawings to show up on the screen.
        '''

        # Get the active screen.  If the turtle is not on the active screen,
        # raise an error.
        active_screen = get_active_screen()
        if active_screen is None or self not in active_screen:
            raise RuntimeError("A Turtle can only move on an active screen!")

        # If the animations are turned off, just use the parent class method.
        if not self._animate:
            Painter.set_position(self, x, y)
            if self._redraw_on_part_step:
                active_screen.redraw()
            return

        # Create vectors for the start and end positions
        current = pygame.Vector2(self._pos)
        end = pygame.Vector2(x, y)

        # Calculate the distance and a vector representing each step
        distance = current.distance_to(end)
        delta_normal = (end - current).normalize()

        # Each iteration of this loop will move the turtle by at most one step
        while distance > 0:
            # If the distance fits in the current step, do the whole thing
            if distance < self._pixels_remaining:
                Painter.set_position(self, end)
                self._pixels_remaining -= distance
                distance = 0
                if self._redraw_on_part_step:
                    active_screen.redraw()

            # Otherwise, just do the rest of the current step and take a break
            # until the next frame
            else:
                current += self._pixels_remaining * delta_normal
                Painter.set_position(self, current)
                distance -= self._pixels_remaining
                self._pixels_remaining = self._step_size
                active_screen.redraw()
                self.clock.tick(self._frame_rate)


    def begin_fill (self, as_moving=True):
        '''
        Start creating a filled shape.

        This function must be followed with a call to end_fill() which
        will draw the filled shape using all of the points visited
        from the call of this method.

        If `as_moving` is set to `True`, then the filled shape will be redrawn
        after each move of the sprite.
        '''

        # By default, a turtle will show fills as it moves.  This is the
        # opposite of a Painter which does not show fills as it moves.
        Painter.begin_fill(self, as_moving)


    def walk_path (self, path):
        '''
        Move the Sprite along a path.

        If a line is currently being drawn, then it will continue from the 
        current position and be drawn along the path.

        The path should be a list of coordinate pairs
        (e.g. `[(100, 0), (-200, 100), (200, -50)]`)
        '''

        # Disable redrawing after each step on the path, so that the screen isn't
        # redrawn multiple times unnecessarily.  Then call the parent walk_path().
        redraw_setting = self._redraw_on_part_step
        self._redraw_on_part_step = False
        Painter.walk_path(self, path)

        # Reset the redraw setting and if it was originally on, redraw the screen
        self._redraw_on_part_step = redraw_setting
        if redraw_setting:
            active_screen = get_active_screen()
            active_screen.redraw()


    def circle (self, radius, extent=360):
        '''
        Draw a circle counterclockwise.

        The circle will have the given `radius`.  If `radius` is negative, then
        the circle is draw clockwise.
        
        The `extent` is used to draw an arc around a portion of a circle.  If 
        `extent` is negative, draw the circle clockwise.

        The circle will actually be an approximation.  The turtle will really
        draw a regular polygon with 360 sides.
        '''

        # Disable redrawing after each step of the circle, so that the screen isn't
        # redrawn multiple times unnecessarily.  Then call the parent circle().
        redraw_setting = self._redraw_on_part_step
        self._redraw_on_part_step = False
        Painter.circle(self, radius, extent)

        # Reset the redraw setting and if it was originally on, redraw the screen
        self._redraw_on_part_step = redraw_setting
        if redraw_setting:
            active_screen = get_active_screen()
            active_screen.redraw()


    def set_speed (self, speed):
        '''
        Change the speed that the turtle moves on the screen.

        The speed must be a positive number.  It is the number of pixels that the
        turtle moves per second.
        '''

        if speed <= 0:
            raise ValueError("The speed must be positive!")
        self._speed = speed
        self._step_size = speed / self._frame_rate


    def get_speed (self):
        '''
        Return the current speed that the turtle moves on the screen.
        '''

        return self._speed


    def enable_animations (self):
        '''
        Enable the turtle's animations.
        '''

        self._animate = True


    def disable_animations (self):
        '''
        Disable the turtle's animations.
        '''

        self._animate = False
