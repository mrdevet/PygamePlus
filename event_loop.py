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
from pygame.locals import *

from screen import Screen

class EventLoopTerminated (Exception):
    pass

class EventLoop (object):

    _active = None

    def __init__ (self, frame_rate=40):
        self._running = False
        self._frame_rate = frame_rate
        self._clicked_sprites = [None for _ in range(5)]

    def set_frame_rate (self, frame_rate):
        self._frame_rate = frame_rate

    def get_frame_rate (self):
        return self._frame_rate

    def set_frame_delay (self, delay):
        self._frame_rate = 1000 / delay

    def get_frame_delay (self):
        return 1000 / self._frame_rate

    def start (self):
        self._running = True
        clock = pygame.time.Clock()
        while self._running:
            # Force the loop to wait if the entire frame delay has not passed 
            # since the start of the last iteration
            clock.tick(self._frame_rate)

            # Get the active screen
            screen = Screen._active

            # Loop through the events that have occurred over the past frame
            for event in pygame.event.get():
                # If the close button is clicked, end the loop
                if event.type == QUIT:
                    _running = False

                # If a custom event occurs, call its handler.  This is generally
                # used for timer events.
                # elif event.type >= USEREVENT:
                #     try:
                #         _custom_events[event.type - USEREVENT]()
                #     except IndexError:
                #         pass

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
                    # TODO: Get Sprite release working
                    button = event.button
                    sprite = self._clicked_sprites[button - 1]
                    if sprite and sprite._release_funcs[button - 1] is not None:
                        # TODO: Make this work with mouse position parameters
                        sprite._release_funcs[button - 1]()
                    self._clicked_sprites[button - 1] = None

                # If the mouse moves and a button is down, call any associated
                # drag handlers
                elif event.type == MOUSEMOTION:
                    # TODO: Get Sprite drag working
                    for button, sprite in enumerate(self._clicked_sprites, 1):
                        if sprite and sprite._drag_funcs[button - 1] is not None:
                            # TODO: Make this work with mouse position parameters
                            sprite._drag_funcs[button - 1]()

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

    def end (self):
        EventLoop._active = None
        self._running = False

    def kill (self):
        EventLoop._active = None
        raise EventLoopTerminated()

def start_event_loop (frame_rate=40):
    loop = EventLoop(frame_rate)
    EventLoop._active = loop
    loop.start()

def end_event_loop ():
    if EventLoop._active is not None:
        EventLoop._active.end()

__all__ = [
    "EventLoop",
    "start_event_loop",
    "end_event_loop"
]
