---
layout: default
title: pygameplus
---
# pygameplus

---

## Member Summary

### Submodules

| <a href="#music_stream">`music_stream`</a> | Pygame module for controlling streamed audio. |

### Classes

| <a href="#Painter">`Painter(image=None)`</a> | A Painter is a special sub-class of a Sprite with extra methods used to  draw on the screen.  All methods of a Sprite object can be used on Painter objects. |
| <a href="#Screen">`Screen(width, height, title='')`</a> | A Screen represents a single game screen visible in the window. |
| <a href="#Sound">`Sound(...)`</a> | Create a new Sound object from a file or buffer object. |
| <a href="#Sprite">`Sprite(image=None)`</a> | A Sprite represents an image that moves around the screen in a game. |
| <a href="#Turtle">`Turtle()`</a> | A Turtle is a special sprite that can move around the screen and make  drawings.  The turtle's movements will be animated so that you can see it's movements. |

### Functions

| <a href="#end_game">`end_game()`</a> | End the event loop. |
| <a href="#from_pygame_coordinates">`from_pygame_coordinates(pygame_x, pygame_y=None)`</a> | Convert a point in the pygame coordinate space to the same point in  the active screen's coordinate space. |
| <a href="#get_active_screen">`get_active_screen()`</a> | Return the currently active screen. |
| <a href="#get_game_loop">`get_game_loop()`</a> | Returns the event loop object. |
| <a href="#load_picture">`load_picture(picture)`</a> | Load a picture into your program. |
| <a href="#start_game">`start_game(frame_rate=None)`</a> | Start the event loop to handle any interactions with the user. |
| <a href="#to_pygame_coordinates">`to_pygame_coordinates(x, y=None)`</a> | Convert a point in the active screen's coordinate space to the same point  in the pygame coordinate space. |

---

## Member Details

### `Painter(image=None)` {#Painter}

> A Painter is a special sub-class of a Sprite with extra methods used to  draw on the screen.  All methods of a Sprite object can be used on Painter objects.
> 
> Some features of Painter objects include:  - They can draw on the screen when they move.  - They can be used to draw filled polygons.  - They can draw dots and circles.  - They can stamp copies of their image to the screen.  - They can write text to the screen.

### `Screen(width, height, title='')` {#Screen}

> A Screen represents a single game screen visible in the window.
> 
> At any one time there can be only one "active" screen that is visible. If a screen is active and another is opened, then the active screen is  replaced in the window.
> 
> Screen objects store the following information about a screen:  - Its dimensions and title  - The background color and/or image  - Any images that have been drawn on the screen
> 
> Methods are provided to do the following:  - Open a screen and make it active  - Change the dimensions, title or background  - Clear any images that have been drawn on the screen  - Add behaviour when the mouse clicks on the screen or when keyboard    keys are used when the screen is active

### `Sound(...)` {#Sound}

> Create a new Sound object from a file or buffer object.
> 
> Wrapper for [`pygame.mixer.Sound`](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound).  See the pygame reference for more details.

### `Sprite(image=None)` {#Sprite}

> A Sprite represents an image that moves around the screen in a game.
> 
> Sprite objects store the following information necessary for drawing these images on the screen:  - The position of the sprite on the screen using coordinates  - The direction that the sprite is pointing using an angle measured    counterclockwise from the positive x-axis.
> 
> Methods are provided for the following:  - Moving and turning the sprite  - Detecting whether or not a sprite is touching other sprites  - Animating the sprite  - Adding behaviour when the mouse interacts with the sprite

### `Turtle()` {#Turtle}

> A Turtle is a special sprite that can move around the screen and make  drawings.  The turtle's movements will be animated so that you can see it's movements.
> 
> A turtle object includes all of the movement methods of a Sprite and the drawing methods of a Painter.

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

> Pygame module for controlling streamed audio.
> 
> Alias for [`pygame.mixer.music`](https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music).  See the pygame reference for more details.

### `start_game(frame_rate=None)` {#start_game}

> Start the event loop to handle any interactions with the user.
> 
> The frame rate is the number of iterations the event loop should try to accomplish in a second.

### `to_pygame_coordinates(x, y=None)` {#to_pygame_coordinates}

> Convert a point in the active screen's coordinate space to the same point  in the pygame coordinate space.

