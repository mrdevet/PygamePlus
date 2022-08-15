# Copyright 2022 Casey Devet
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

from .painter import *
from .screen import get_active_screen
from .gameloop import get_game_loop

################################################################################
#                                 TURTLE CLASS
################################################################################

class Turtle (Painter):
    '''
    A Turtle is a special sprite that can move around the screen and make 
    drawings.  When you move the turtle using any of its methods, it
    will be automatically animated.

    A turtle object includes all of the movement methods of a Sprite 
    and the drawing methods of a Painter.
    '''

    _game_loop = get_game_loop()

    def __init__ (self):
        '''
        Create a Turtle object.
        '''

        # The attributes used to animate the turtle
        self._speed = 120
        self._step_size = 120 / self._game_loop._frame_rate
        self._animate = True

        # Attributes that allow the speed to be maintained over multiple changes
        # to position
        self._animate_queue = []
        self._pixels_remaining = 0
        self._terminate_game_loop = False

        Painter.__init__(self, "turtle")

        # Set that the turtle image should rotate when the turtle turns and
        # draw incomplete fills on the screen.
        self.rotates = True
        self.fill_as_moving = True


    def __setattr__ (self, name, value):
        if name in ['_dirty_rotate', '_dirty_scale', '_dirty_flip', '_dirty_canvas', '_dirty_visible'] and value is True and not self._game_loop.running:
            active_screen = get_active_screen()
            if active_screen is not None:
                if name == '_dirty_visible' or self in active_screen:
                    active_screen.draw()
                    pygame.display.flip()
        super().__setattr__(name, value)


    ### Animation properties

    @property
    def speed (self):
        '''
        The current speed (in pixels per second) that the turtle moves on 
        the screen.
        '''

        return self._speed

    @speed.setter
    def speed (self, new_speed):

        # Ensure that the speed is a number
        try:
            new_speed = float(new_speed)
        except:
            raise ValueError("The speed must be a number!") from None

        # Ensure that the speed is positive
        if new_speed <= 0:
            raise ValueError("The speed must be positive!")

        # Set the speed and the step size
        self._speed = new_speed
        self._step_size = new_speed / self._game_loop._frame_rate


    @property
    def animate (self):
        '''
        Whether or not the turtle's movements will be animated.

        If set to False, movements will happen instantaneously.
        '''

        return self._animate

    @animate.setter
    def animate (self, is_animated):

        self._animate = bool(is_animated)


    def turn_to (self, direction, reverse=False):
        '''
        Turn the sprite to the point at the given `direction`.

        The direction is an angle (in degrees) counterclockwise from the
        positive x-axis.  Here are some important directions:
         - 0 degrees is directly to the right
         - 90 degrees is directly up
         - 180 degrees is directly to the left
         - 270 degrees is directly down
         '''

        # If the animations are turned off, just use the parent 
        # class method.
        if not self._animate:
            super().turn_to(direction, reverse=reverse)
            return

        # Calculate the arc length of the rotation of the turtle's head
        current = self._dir
        end = (direction + 180) % 360 if reverse else direction
        angle_change = (end - current + 180) % 360 - 180
        arc_length = self._scale * math.pi * abs(angle_change) / 15
        pixel_angle = 15 / math.pi / self._scale
        if angle_change < 0:
            pixel_angle = -pixel_angle

        # If we still have sufficient pixels in the frame, just move
        if arc_length <= self._pixels_remaining:
            Painter.direction.fset(self, end)
            self._pixels_remaining -= arc_length
            return

        # If there are pixels remaining in the frame, use them up
        elif self._pixels_remaining > 0:
            current = current + self._pixels_remaining * pixel_angle
            Painter.direction.fset(self, current)
            arc_length -= self._pixels_remaining
            self._pixels_remaining = 0

        # Find all of the remaining steps that need to be queued
        while arc_length > 0:
            # If there is only a bit left, queue it with pixels remaining
            if arc_length < self._step_size:
                self._animate_queue.append((self._pos, end, self._step_size - arc_length))
                arc_length = 0

            # Otherwise, queue a whole step
            else:
                current = current + self._step_size * pixel_angle
                self._animate_queue.append((self._pos, current, 0))
                arc_length -= self._step_size

        # If the game loop is not running, start it up to animate
        # this move
        if not self._game_loop.running:
            self._terminate_game_loop = True
            self._game_loop.start()


    def go_to (self, x, y=None, turn=True, reverse=False):
        '''
        Turn the sprite and move the sprite to the given coordinates.

        Unlike changing the position property, this method will also turn the
        sprite in the direction of the given location.  This behaviour can be
        turned off by setting the `turn` argument to `False`.
        '''

        # If the animations are turned off, just use the parent 
        # class method.
        if not self._animate:
            super().go_to(x, y, turn=turn, reverse=reverse)
            return

        # Create vectors for the start and end positions
        current = pygame.Vector2(self._pos)
        end = pygame.Vector2(x, y)

        # Calculate the distance and direction to the point
        delta = end - current
        distance, direction = delta.as_polar()
        delta_normal = delta.normalize()

        # If turning to go to the point, animate the turn as well
        if turn:
            self.turn_to(direction, reverse=reverse)
            if reverse:
                direction = (direction + 180) % 360
        else:
            direction = self._dir

        # If we still have sufficient pixels in the frame, just move
        if distance <= self._pixels_remaining:
            Painter.position.fset(self, end)
            self._pixels_remaining -= distance
            return

        # If there are pixels remaining in the frame, use them up
        elif self._pixels_remaining > 0:
            current = current + self._pixels_remaining * delta_normal
            Painter.position.fset(self, current)
            distance -= self._pixels_remaining
            self._pixels_remaining = 0

        # Find all of the remaining steps that need to be queued
        while distance > 0:
            # If there is only a bit left, queue it with pixels remaining
            if distance < self._step_size:
                self._animate_queue.append((end, direction, self._step_size - distance))
                distance = 0

            # Otherwise, queue a whole step
            else:
                current = current + self._step_size * delta_normal
                self._animate_queue.append((current, direction, 0))
                distance -= self._step_size

        # If the game loop is not running, start it up to animate
        # this move
        if not self._game_loop.running:
            self._terminate_game_loop = True
            self._game_loop.start()


    def update (self, screen=None):
        '''
        Update the sprite in preparation to draw the next frame.

        This method should generally not be called explicitly, but will be called
        by the event loop if the sprite is on the active screen.
        '''

        # At the beginning of the frame, we need to leave room for
        # possible small movements that don't require another frame
        self._pixels_remaining = self._step_size

        # If there are animations queue, complete one frame of them
        while self._animate_queue:
            new_pos, new_dir, pixels_left = self._animate_queue.pop(0)
            Painter.direction.fset(self, new_dir)
            Painter.position.fset(self, new_pos)
            self._pixels_remaining = pixels_left
            if not pixels_left:
                break

        # If there are no more animations and the game loop is only
        # running for this turtle, kill it.
        if self._terminate_game_loop and not self._animate_queue:
            self._terminate_game_loop = False
            self._game_loop.stop()

        # Call parent update method
        super().update(screen)


# What is included when importing *
__all__ = [
    "Turtle",
    "Color"
]
