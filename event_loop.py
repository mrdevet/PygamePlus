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

import pygame
from pygame.locals import *

from screen import get_active_screen

################################################################################
#                               EVENTLOOP CLASS
################################################################################

class EventLoopTerminated (Exception):
    '''
    Will be raised when the event loop is killed.
    '''

    pass

class EventLoop (object):
    '''
    An EventLoop represents the loop that is continuously running in the
    background of a game and handles any events that occur.

    EventLoop objects store the following information about an event loop:
     - Whether or not the event loop is running
     - The frame rate that the loop should try to maintain

    Methods are provided for the following:
     - To get or change the frame rate
     - To start and stop the loop
    '''

    def __init__ (self, frame_rate=40):
        '''
        Create an EventLoop object.

        EventLoop objects should generally not be created explicitly using the
        EventLoop() constructor.  Instead, use the start_event_loop() and
        end_event_loop() functions.
        '''

        # Attributes that store the event loops current state
        self._running = False
        self._frame_rate = frame_rate

        # Attribute to hold which sprites are currently being clicked on
        self._clicked_sprites = [None for _ in range(5)]

        # Attribute to hold custom event handlers
        self._timers = {}


    def set_frame_rate (self, frame_rate):
        '''
        Change the frame rate of the event loop.

        The frame rate is the number of iterations the event loop should try to
        accomplish in a second.
        '''

        self._frame_rate = frame_rate


    def get_frame_rate (self):
        '''
        Return the current frame rate of the event loop.
        '''

        return self._frame_rate


    def set_frame_delay (self, delay):
        '''
        Change the frame delay of the event loop.

        The frame delay is the amount of time in milliseconds that the event loop
        should try to have between the start of each iteration of the loop.  The
        frame delay is 1000 divided by the frame rate.
        '''

        self._frame_rate = 1000 / delay


    def get_frame_delay (self):
        '''
        Return the current frame delay of the event loop.
        '''

        return 1000 / self._frame_rate


    def start (self):
        '''
        Start the event loop.
        '''

        self._running = True
        clock = pygame.time.Clock()
        while self._running:
            # Force the loop to wait if the entire frame delay has not passed 
            # since the start of the last iteration
            clock.tick(self._frame_rate)

            # Get the active screen
            screen = get_active_screen()
            if screen is None:
                continue

            # Loop through the events that have occurred over the past frame
            for event in pygame.event.get():
                # If the close button is clicked, end the loop
                if event.type == QUIT:
                    self._running = False
                    pygame.display.quit()
                    return

                # If a key was pressed, call any associated handlers
                elif event.type == KEYDOWN:
                    if event.key in screen._key_press_funcs:
                        screen._key_press_funcs[event.key]()
                    elif None in screen._key_release_funcs:
                        screen._key_press_funcs[None]()

                # If a key was released, call any associated handlers
                elif event.type == KEYUP:
                    if event.key in screen._key_release_funcs:
                        screen._key_release_funcs[event.key]()
                    elif None in screen._key_release_funcs:
                        screen._key_release_funcs[None]()

                # If a mouse button is clicked down, call any associated handlers
                elif event.type == MOUSEBUTTONDOWN:
                    button = event.button
                    for sprite in screen:
                        if sprite.rect.collidepoint(event.pos):
                            self._clicked_sprites[button - 1] = sprite
                            # TODO: Make this work with mouse position parameters
                            if sprite._click_funcs[button - 1] is not None:
                                sprite._click_funcs[button - 1]()
                            break
                    if screen._click_funcs[button - 1] is not None:
                        # TODO: Make this work with mouse position parameters
                        screen._click_funcs[button - 1]()

                # If a mouse button is released, call any associated handlers
                elif event.type == MOUSEBUTTONUP:
                    button = event.button
                    sprite = self._clicked_sprites[button - 1]
                    if sprite and sprite._release_funcs[button - 1] is not None:
                        # TODO: Make this work with mouse position parameters
                        sprite._release_funcs[button - 1]()
                    self._clicked_sprites[button - 1] = None

                # If the mouse moves and a button is down, call any associated
                # drag handlers
                elif event.type == MOUSEMOTION:
                    for button, sprite in enumerate(self._clicked_sprites, 1):
                        if sprite and sprite._drag_funcs[button - 1] is not None:
                            # TODO: Make this work with mouse position parameters
                            sprite._drag_funcs[button - 1]()

                # If a custom event occurs, call its handler.  This is generally
                # used for timer events.
                elif event.type in self._timers:
                    self._timers[event.type]()

            # Get a dictionary containing the state of the keyboard keys
            keys = pygame.key.get_pressed()
            key_count = keys.count(1)

            # Loop through the keyhold handlers and call any for which the 
            # key is down
            try:
                for key_code, func in screen._key_hold_funcs.items():
                    if key_code is None and key_count > 0:
                        func()
                    elif key_code is not None and keys[key_code]:
                        func()
            except RuntimeError:
                pass

            # Update the active screen
            screen.update()
            screen.draw()
            pygame.display.flip()


    def end (self):
        '''
        End the event loop.

        This does not immediately end the event loop, but will end the loop at the end of the current iteration.
        
        This will have no effect if the event loop has not started.
        '''

        self._running = False


    def kill (self):
        '''
        Terminate the event loop immediately.

        This will raise an EventLoopTerminated exception.
        '''

        raise EventLoopTerminated()


    def on_timer (self, func, delay, repeat=False):
        '''
        Call a function after a given amount of time (in milliseconds).

        The function `func` will be called after `delay` milliseconds.  `func`
        must be a function that takes no arguments.  The `delay` must be a 
        positive number.

        If `repeat` is `True`, then the timer will run repeatedly.  That is,
        the timer will restart every time that it expires.

        An event ID will be returned that can be used with the `cancel_timer()`
        method to stop the timer.
        '''

        # Check that the arguments are valid
        if not callable(func):
            raise ValueError("The function is not callable!")
        if delay <= 0:
            raise ValueError("The delay must be positive!")

        # Get a custom pygame event type and start the timer
        event_id = pygame.event.custom_type()
        self._timers[event_id] = func
        pygame.time.set_timer(event_id, delay, not repeat)

        # Return the custom event type for cancelling
        return event_id


    def cancel_timer (self, event_id):
        '''
        Stop the timer with the given event ID.

        `event_id` must be an event ID that was returned from the `on_timer()`
        method for this EventLoop.
        '''

        # Check that the argument is a valid event type
        if event_id not in self._timers:
            raise ValueError("There is no global timer with that event ID!")

        # Stop the timer
        pygame.time.set_timer(event_id, 0)
        self._timers.pop(event_id)


################################################################################
#                               GLOBAL FUNCTIONS
################################################################################

# Creates and EventLoop instance to use with the functions below.
_event_loop = EventLoop()

def start_event_loop (frame_rate=None):
    '''
    Start the event loop to handle any interactions with the user.

    The frame rate is the number of iterations the event loop should try to
    accomplish in a second.
    '''

    if frame_rate is not None:
        _event_loop.set_frame_rate(frame_rate)
    _event_loop.start()


def end_event_loop ():
    '''
    End the event loop.

    This does not immediately end the event loop, but will end the loop at the 
    end of the current iteration.
        
    This will have no effect if the event loop has not started.
    '''

    _event_loop.end()


def get_event_loop ():
    '''
    Returns the event loop object.

    This is really only necessary if you need to change the frame rate of the
    event loop while it is running or it you need to kill the event loop.
    '''

    return _event_loop


# What is included when importing *
__all__ = [
    "start_event_loop",
    "end_event_loop",
    "get_event_loop"
]
