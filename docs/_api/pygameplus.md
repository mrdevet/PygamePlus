---
layout: default
title: pygameplus
---
# pygameplus

## Submodules

| Module | Description |
| --- | --- |
| music_stream | pygame module for controlling streamed audio |

## Classes

| Class | Description |
| --- | --- |
| Color | Color(r, g, b) -> Color<br />Color(r, g, b, a=255) -> Color<br />Color(color_value) -> Color<br />pygame object for color representations |
| Painter | A Painter is a special sub-class of a Sprite with extra methods used to <br />draw on the screen.  All methods of a Sprite object can be used on<br />Painter objects. |
| Screen | A Screen represents a single game screen visible in the window. |
| Sound | Sound(filename) -> Sound<br />Sound(file=filename) -> Sound<br />Sound(file=pathlib_path) -> Sound<br />Sound(buffer) -> Sound<br />Sound(buffer=buffer) -> Sound<br />Sound(object) -> Sound<br />Sound(file=object) -> Sound<br />Sound(array=object) -> Sound<br />Create a new Sound object from a file or buffer object |
| Sprite | A Sprite represents an image that moves around the screen in a game. |
| Turtle | A Turtle is a special sprite that can move around the screen and make <br />drawings.  The turtle's movements will be animated so that you can see it's<br />movements. |

## Functions

| Function | Description |
| --- | --- |
| end_game() | End the event loop. |
| from_pygame_coordinates(pygame_x, pygame_y=None) | Convert a point in the pygame coordinate space to the same point in <br />the active screen's coordinate space. |
| get_active_screen() | Return the currently active screen. |
| get_game_loop() | Returns the event loop object. |
| load_picture(picture) | Load a picture into your program. |
| start_game(frame_rate=None) | Start the event loop to handle any interactions with the user. |
| to_pygame_coordinates(x, y=None) | Convert a point in the active screen's coordinate space to the same point <br />in the pygame coordinate space. |

## Function Details

### `end_game()`

End the event loop.

This does not immediately end the event loop, but will end the loop at the <br />end of the current iteration.<br />    <br />This will have no effect if the event loop has not started.

### `from_pygame_coordinates(pygame_x, pygame_y=None)`

Convert a point in the pygame coordinate space to the same point in <br />the active screen's coordinate space.

### `get_active_screen()`

Return the currently active screen.

This will return None if no screen is active.

### `get_game_loop()`

Returns the event loop object.

This is really only necessary if you need to change the frame rate of the<br />event loop while it is running or it you need to kill the event loop.

### `load_picture(picture)`

Load a picture into your program.

This is useful if you will be changing the picture of a Sprite often.<br />You can load the picture once and then change the picture to this<br />object.

This function returns a pygame Surface.

### `start_game(frame_rate=None)`

Start the event loop to handle any interactions with the user.

The frame rate is the number of iterations the event loop should try to<br />accomplish in a second.

### `to_pygame_coordinates(x, y=None)`

Convert a point in the active screen's coordinate space to the same point <br />in the pygame coordinate space.

## Other Attributes

| Name | Description |
| --- | --- |
| x | int([x]) -> integer<br />int(x, base=10) -> integer |

