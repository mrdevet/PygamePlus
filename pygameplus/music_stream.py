'''
Pygame module for controlling streamed audio.

Alias for [`pygame.mixer.music`](https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music).  See the pygame reference for more details.
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

import pygame
from pygame.mixer_music import *

__all__ = [
    'fadeout',
    'get_busy',
    'get_endevent',
    'get_pos',
    'get_volume',
    'load',
    'pause',
    'play',
    'queue',
    'rewind',
    'set_endevent',
    'set_pos',
    'set_volume',
    'stop',
    'unload',
    'unpause',
    'x'
]

_EXTERNAL_DOCS = {}
for attr in __all__:
    _EXTERNAL_DOCS[attr] = f'https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.{attr}'
