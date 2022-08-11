'''
PygamePlus

**TODO**
'''

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

__version__ = "0.0.1"

# Remove PyGame load message in console
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

pygame.init()

from .screen import *
from .sprite import *
from .painter import *
from .turtle import *
from .gameloop import *
from .pgputils import *
from . import music_stream

class Sound (pygame.mixer.Sound):
    '''
    Create a new Sound object from a file or buffer object.
    
    Wrapper class for [`pygame.mixer.Sound`](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound).  See the pygame reference for more details.
    '''

    # Set external links for inherited attributes
    _EXTERNAL_DOCS = {}
    for attr in dir(pygame.mixer.Sound):
        _EXTERNAL_DOCS[attr] = f'https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound.{attr}'
    del attr


__all__ = [
    'Painter', 
    'Screen', 
    'Sound',
    'Sprite', 
    'Turtle', 
    'from_pygame_coordinates', 
    'get_active_screen', 
    'get_game_loop', 
    'load_picture', 
    'music_stream',
    'start_game', 
    'end_game', 
    'to_pygame_coordinates'
]