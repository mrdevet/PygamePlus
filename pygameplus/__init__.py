
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

class Sound (pygame.mixer.Sound):
    '''
    Create a new Sound object from a file or buffer object.
    
    Wrapper for [`pygame.mixer.Sound`](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound).  See the pygame reference for more details.
    '''
    pass

music_stream = pygame.mixer.music
music_stream.__doc__ = '''
    Pygame module for controlling streamed audio.

    Alias for [`pygame.mixer.music`](https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music).  See the pygame reference for more details.
    '''


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
    'to_pygame_coordinates',
    'x'
]