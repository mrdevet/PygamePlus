---
nav_order: 2
---
# Sprite

A Sprite represents an image that moves around the screen in a game.

Sprite objects store the following information necessary for drawing these images on the screen:
 - The position of the sprite on the screen using coordinates
 - The direction that the sprite is pointing using an angle measured counterclockwise from the positive x-axis.

Methods are provided for the following:
 - Moving and turning the sprite
 - Detecting whether or not a sprite is touching other sprites
 - Animating the sprite
 - Adding behaviour when the mouse interacts with the sprite

## Creation

To create a sprite, you must provide an image for it.

```python
# Create a screen that is 540px wide and 360px high
my_character = Sprite('dog.png')
```

Note that creating a sprite does not display it on a screen.  You must use add it to the screen for it to appear.

## Sprite Groups and Screens

| Property/Method | Description |
| --- | --- |
| `.visible` | Whether or not the sprite is on the active screen. |
| `.hide()` | Remove the sprite from the active screen. |
| `.show()` | Adds the sprite to the active screen. |
| `.kill()` | Removes the sprite from all groups and screens. |
| `.layer` | The layer at which the sprite is located on the screen.  This is readonly. |

## Image

A sprite's image can be adjusted and altered in many ways using the properties below.

| Property | Description |
| --- | --- |
| `.picture` | The sprite's picture.  Change the sprite's image by changing this property. |
| `.height` | The height of the sprite's image.  This value will change if the image is rotated.  Changing this property will also change the width to maintain the same ratio. |
| `.width` | The width of the sprite's image.  This value will change if the image is rotated.  Changing this property will also change the height to maintain the same ratio. |
| `.size` | A tuple containing the width and height.  This is readonly. |
| `.scale_factor` | The factor by which the image's dimensions are scaled from the original image.  (default: `1`) |
| `.rotates` | Whether or not the image rotates when the sprite changes direction.  (default: `False`) |
| `.tilt` | The angle that the image is tilted counterclockwise from its original orientation.  If image rotation is on, then this will be the angle the image is tilted from the original when the direction is 0 degrees. |
| `.smooth` | Whether or not the image is smoothed when scaled or rotated.  Turning on smoothing can decrease performance if the image will be transformed often.  (default: `False`) |
| `.flipped_horizontally` | Whether or not the original image is flipped horizontally.  (default: `False`) |
| `.flipped_vertically` | Whether or not the original image is flipped vertically.  (default: `False`) |
| `.flipped` | A tuple containing whether or not the image is flipped horizontally and vertically. |
| `.opacity` | A number representing how transparent the image is on a scale from 0 (fully transparent) to 1 (fully opaque).  (default: `1`) |

## Position and Direction

| Property | Description |
| --- | --- |
| `.x` | The x-coordinate of the sprite on the screen. (default: `0`) |
| `.y` | The y-coordinate of the sprite on the screen. (default: `0`) |
| `.position` | A tuple containing the coordinates (x, y) of the sprite on the screen. (default: `(0, 0)`) |
| `.direction` | The current direction that the sprite is pointing.  The direction is an angle in degrees measured counterclockwise from a line directly right of the sprite. (default: `0`) |
| `.anchor` | The point on the image that will be placed on the sprite's exact position and used as the center of gravity for scaling and rotating.  It is a 2-tuple that contains a coordinate relative to the center of the image, a description (e.g. `'center'`, `'left'`, `'right'`, `'top'`, `'bottom'`) or a combination of the two. (default: `('center', 'center')`) |

### Other Position Properties

A sprite's position can also be accessed using these properties which represent points on the image: 
 - `.center`
 - `.bottom_left_corner`
 - `.bottom_right_corner`
 - `.top_left_corner`
 - `.top_right_corner`
 - `.bottom_edge_midpoint`
 - `.left_edge_midpoint`
 - `.right_edge_midpoint`
 - `.top_edge_midpoint`

The following properties can be used to access one coordinate of some location on the image: 
 - `.center_x`
 - `.center_y`
 - `.bottom_edge`
 - `.left_edge`
 - `.right_edge`
 - `.top_edge` 

## Movement

The following methods can be used to change the position and/or direction of the sprite.

| Method | Description |
| --- | --- |
| `.move_forward(distance)` | Move the sprite by the given distance in the direction it is currently pointing. |
| `.move_backward(distance)` | Move the sprite by the given distance in the opposite of the direction it is currently pointing. |
| `.go_to(x, y)` | Turn the sprite towards the given coordinates, then move there. |
| `.turn_left(angle)` | Turn the sprite left (counterclockwise) by the given angle. |
| `.turn_right(angle)` | Turn the sprite right (clockwise) by the given angle. |
| `.turn_toward(x, y)` | Turn the sprite to be facing towards a given point. |

## Animation

PygamePlus programs use a game loop that runs in the background and handles events and updates the screen.  To animate sprites, we can provide a function that will be called every iteration of the game loop that updates the sprite and makes it look like it is moving or changing.

| Method | Description |
| --- | --- |
| `.on_update(func)` | Bind a function that will be executed every iteration of the game loops to animate the sprite.  The update function can take one argument, called `sprite`, which can be used to access the sprite's current state. |

## Event Handlers

Event handler functions may be bound to the sprite to be executed when mouse events occur in connection to the sprite.

The methods below are used to bind event handler functions to these events.  If the function provided has certain named arguments, they will be used to pass event information (e.g. mouse location, key) to the handler.

| Property/Method | Description |
| --- | --- |
| `.on_click(func, button='left', method='rect', bleeds=False)` | Bind a function to mouse click down events on the sprite.  Optionally, you can specify which mouse button to bind to (`'left'`, `'right'`, `'middle'`, `'scrollup'`, `'scrolldown'`).  You may also specify which collision detection method should be used (see below).  Finally, you may also specify whether or not the event bleeds down to any sprites below this one on the screen.  The handler function can have these arguments: `x`, `y`, `pos`, `button`, `sprite`. |
| `.on_drag(func, button='left')` | Bind a function to mouse movement while the mouse is clicked on the sprite.  Optionally, you can specify which mouse button to bind to (`'left'`, `'right'`, `'middle'`, `'scrollup'`, `'scrolldown'`).  The handler function can have these arguments: `x`, `y`, `pos`, `button`, `sprite`. |
| `.on_release(func, button='left')` | Bind a function to mouse button release after the sprite has been clicked on.  Optionally, you can specify which mouse button to bind to (`'left'`, `'right'`, `'middle'`, `'scrollup'`, `'scrolldown'`).  The handler function can have these arguments: `x`, `y`, `pos`, `button`, `sprite`. |
| `.disabled` | If this property is set to `True`, then all mouse events will be ignored. (default: `False`) |

## Other Sprites and Collision Detection

The following methods can be used to compare a sprite's position with that of another sprite or to detect collisions (when sprites are touching).

| Method | Description |
| --- | --- |
| `.get_direction_to(other)` | Returns the direction this sprite must turn to to be pointing directly at the other sprite. |
| `.get_distance_to(other)` | Returns the distance between this sprite's position and the other sprite's. |
| `.is_touching(other, method='rect')` | Returns whether or not this sprite is touching the other sprite (or collection of sprites).  See below for the available methods. |
| `.get_touching(others, method='rect')` | Takes a collection of sprites and returns the subset that this sprites is touching.  See below for the available methods. |
| `.is_touching_point(x, y, method='rect')` | Returns whether or not this sprite is in collision with a single given point.  See below for the avialable methods. |

### Collision Detection Methods

PygamePlus include three different built-in methods for collision detection:
 - `'rect'` (default) - A collision occurs when the rectangles around the sprites' images are overlapping.
 - `'circle'` - A collision occurs when circles centered at the sprites' positions are overlapping.  To use circle collisions effectively, you need to set the `.radius` attribute on the sprites.
 - `'mask'` - A collision occurs when the non-transparent parts of the sprites' images are overlapping.  This method can reduce performance when sprites are scaled or rotated often.

The method can also be a custom function that takes two sprites as arguments and returns `True` or `False`.

## Updating the Sprite

The following method is provided to update the sprite.  **This function should not be used explicitly, but will be called by the game loop.**

| Property/Method | Description |
| --- | --- |
| `.update(screen=None)` | Update the sprite in preparation to draw the next frame. |