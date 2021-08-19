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

from functools import wraps
import math
import pygame

from pygameplus.painter import *
from pygameplus.screen import get_active_screen

################################################################################
#                                REDRAWMETACLASS
################################################################################

# This function adds a wrapper around a method that will make it so that when
# the method is complete, the active screen will be redraw if the sprite is 
# on that screen.

def add_redraw (method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        active_screen = get_active_screen()
        on_screen_before = active_screen is not None and self in active_screen
        method(self, *args, **kwargs)
        on_screen_after = active_screen is not None and self in active_screen
        if getattr(self, "_redraw_on_completion", True):
            if on_screen_before or on_screen_after:
                active_screen.redraw()
    return wrapper

# This function adds a wrapper around a method that will make it so that any
# intermediate calls to functions wrapped with the add_redraw function above
# don't redraw on completion.

def disable_intermediate_redraw (method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        redraw_on_changes = getattr(self, "_redraw_on_completion", True)
        self._redraw_on_completion = False
        method(self, *args, **kwargs)
        self._redraw_on_completion = redraw_on_changes
    return wrapper

# This metaclass is used to create a class that wraps its methods (and/or its 
# parents' methods) using the above functions.  Include lists called
# add_redraw_methods and disable_intermediate_redraw_methods in the class
# definition of a class using this metaclass.  These lists should hold the names
# of the methods to wrapp with add_redraw and disable_intermediate_redraw,
# respectively.

class RedrawMetaClass (type):

    def __new__ (cls, name, bases, class_dict):
        new_class_dict = class_dict.copy()

        # Wrap the methods in disable_intermediate_redraw_methods
        disable_intermediate_redraw_methods = new_class_dict.pop("disable_intermediate_redraw_methods", [])
        for method_name in disable_intermediate_redraw_methods:
            method = None
            if method_name in new_class_dict:
                method = new_class_dict[method_name]
            else:
                for base in bases:
                    if hasattr(base, method_name):
                        method = getattr(base, method_name)
                        break
            if method is not None:
                new_class_dict[method_name] = disable_intermediate_redraw(method)

        # Wrap the methods in add_redraw_methods
        add_redraw_methods = new_class_dict.pop("add_redraw_methods", [])
        for method_name in add_redraw_methods:
            method = None
            if method_name in new_class_dict:
                method = new_class_dict[method_name]
            else:
                for base in bases:
                    if hasattr(base, method_name):
                        method = getattr(base, method_name)
                        break
            if method is not None:
                new_class_dict[method_name] = add_redraw(method)
        
        return type.__new__(cls, name, bases, new_class_dict)


################################################################################
#                                 TURTLE CLASS
################################################################################

class Turtle (Painter, metaclass=RedrawMetaClass):
    '''
    A Turtle is a special sprite that can move around the screen and make 
    drawings.  The turtle's movements will be animated so that you can see it's
    movements.

    A turtle object includes all of the movement methods of a Sprite and the
    drawing methods of a Painter.
    '''

    # These methods will be changed to disable active screen redraw on any 
    # intermediate calls they make
    disable_intermediate_redraw_methods = [
        "circle",
        "walk_path",
        "go_to"
    ]

    # These methods will be changed to redraw the active screen on completion
    add_redraw_methods = [
        "add",
        "set_position",
        "go_to",
        "set_direction",
        "turn_to",
        "circle",
        "walk_path",
        "show",
        "hide",
        "scale",
        "scale_width",
        "scale_height",
        "set_image_rotates",
        "set_image_tilt",
        "set_color",
        "set_line_color",
        "set_fill_color",
        "end_fill",
        "dot",
        "stamp",
        "write"
    ]

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

        # Set that the turtle image should rotate when the turtle turns and
        # draw incomplete fills on the screen.
        self.rotates = True
        self.fill_as_moving = True

        # Attributes that allow the speed to be maintained over multiple calls 
        # to set_position()
        self._pixels_remaining = 4


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


    def set_position (self, x, y=None):
        '''
        Move the Turtle to the given coordinates.

        If the sprite is currently drawing a line or fill, movement will cause
        drawings to show up on the screen.
        '''

        # Get the active screen.
        active_screen = get_active_screen()

        # If the animations are turned off, just use the parent class method.
        if not self._animate:
            Painter.set_position(self, x, y)
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

            # Otherwise, just do the rest of the current step and take a break
            # until the next frame
            else:
                current += self._pixels_remaining * delta_normal
                Painter.set_position(self, current)
                distance -= self._pixels_remaining
                self._pixels_remaining = self._step_size
                if active_screen is not None and self in active_screen:
                    active_screen.redraw()
                self.clock.tick(self._frame_rate)


    def set_direction (self, direction):
        '''
        Change the direction that the sprite is pointing.

        The direction is an angle (in degrees) counterclockwise from the 
        positive x-axis.  Here are some important directions:
         - 0 degrees is directly to the right
         - 90 degrees is directly up
         - 180 degrees is directly to the left
         - 270 degrees is directly down

        If the given direction is an angle larger than the current direction,
        the turtle will turn left.  If it is smaller, than the turtle will turn
        right.
        '''

        # Get the active screen.
        active_screen = get_active_screen()

        # If the animations are turned off, just use the parent class method.
        if not self._animate:
            Painter.set_direction(self, direction)
            return

        # Calculate the arc length of the rotation of the turtle's head
        arc_length = self._scale.x * 5 * (direction - self._dir) / 18

        # Each iteration of this loop will turn so that it's head moves on an
        # arc that is at most one step
        while arc_length != 0:
            # If the arc_length fits in the current step, do the whole thing
            if abs(arc_length) < self._pixels_remaining:
                Painter.set_direction(self, direction)
                self._pixels_remaining -= arc_length
                arc_length = 0

            # Otherwise, just do the rest of the current step and take a break
            # until the next frame
            else:
                turn_arc_length = 3.6 * self._pixels_remaining / self._scale.x
                if arc_length > 0:
                    Painter.set_direction(self, self._dir + turn_arc_length)
                    arc_length -= self._pixels_remaining
                else:
                    Painter.set_direction(self, self._dir - turn_arc_length)
                    arc_length += self._pixels_remaining
                self._pixels_remaining = self._step_size
                if active_screen is not None and self in active_screen:
                    active_screen.redraw()
                self.clock.tick(self._frame_rate)


# What is included when importing *
__all__ = [
    "Turtle",
    "Color"
]