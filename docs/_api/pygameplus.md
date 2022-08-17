---
layout: default
title: pygameplus
has_children: true
---
# pygameplus

PygamePlus

**TODO**

---

## Member Summary

### Classes

| <a href="../pygameplus.MusicStream">`MusicStream()`</a> | A MusicStream is a queue that manages a collection of music to be streamed during the game.  Music is loaded in chunks for efficiency and the next track is pre-loaded for a seemless transition. |
| <a href="../pygameplus.Painter">`Painter(image=None)`</a> | A Painter is a special sub-class of a Sprite with extra methods used to  draw on the screen.  All methods of a Sprite object can be used on Painter objects. |
| <a href="../pygameplus.Screen">`Screen(width, height, title='')`</a> | A Screen represents a single game screen visible in the window. |
| <a href="../pygameplus.Sound">`Sound(...)`</a> | Create a new Sound object from a file or buffer object. |
| <a href="../pygameplus.Sprite">`Sprite(image=None)`</a> | A Sprite represents an image that moves around the screen in a game. |
| <a href="../pygameplus.Turtle">`Turtle()`</a> | A Turtle is a special sprite that can move around the screen and make  drawings.  When you move the turtle using any of its methods, it will be automatically animated. |

### Functions

| <a href="#end_game">`end_game()`</a> | End the event loop. |
| <a href="#from_pygame_coordinates">`from_pygame_coordinates(pygame_x, pygame_y=None)`</a> | Convert a point in the pygame coordinate space to the same point in  the active screen's coordinate space. |
| <a href="#get_active_screen">`get_active_screen()`</a> | Return the currently active screen. |
| <a href="#get_game_loop">`get_game_loop()`</a> | Returns the event loop object. |
| <a href="#load_picture">`load_picture(picture)`</a> | Load a picture into your program. |
| <a href="#start_game">`start_game(frame_rate=None)`</a> | Start the event loop to handle any interactions with the user. |
| <a href="#to_pygame_coordinates">`to_pygame_coordinates(x, y=None)`</a> | Convert a point in the active screen's coordinate space to the same point  in the pygame coordinate space. |

### Other Members

| <a href="#music_stream">`music_stream`</a> | The queue that manages streaming larger music files.  See the `MusicStream` class for details. |

---

## Member Details

### `end_game()` {#end_game}

> End the event loop.
> 
> This does not immediately end the event loop, but will end the loop at the  end of the current iteration.      This will have no effect if the event loop has not started.

### `from_pygame_coordinates(pygame_x, pygame_y=None)` {#from_pygame_coordinates}

> Convert a point in the pygame coordinate space to the same point in  the active screen's coordinate space.

### `get_active_screen()` {#get_active_screen}

> Return the currently active screen.
> 
> This will return None if no screen is active.

### `get_game_loop()` {#get_game_loop}

> Returns the event loop object.
> 
> This is really only necessary if you need to change the frame rate of the event loop while it is running or it you need to kill the event loop.

### `load_picture(picture)` {#load_picture}

> Load a picture into your program.
> 
> This is useful if you will be changing the picture of a Sprite often. You can load the picture once and then change the picture to this object.
> 
> This function returns a pygame Surface.

### `music_stream` {#music_stream}

> The queue that manages streaming larger music files.  See the `MusicStream` class for details.

### `start_game(frame_rate=None)` {#start_game}

> Start the event loop to handle any interactions with the user.
> 
> The frame rate is the number of iterations the event loop should try to accomplish in a second.

### `to_pygame_coordinates(x, y=None)` {#to_pygame_coordinates}

> Convert a point in the active screen's coordinate space to the same point  in the pygame coordinate space.

