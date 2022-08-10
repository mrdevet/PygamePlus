---
layout: default
title: Painter
parent: pygameplus
---
# Painter

A Painter is a special sub-class of a Sprite with extra methods used to <br />draw on the screen.  All methods of a Sprite object can be used on<br />Painter objects.

Some features of Painter objects include:<br /> - They can draw on the screen when they move.<br /> - They can be used to draw filled polygons.<br /> - They can draw dots and circles.<br /> - They can stamp copies of their image to the screen.<br /> - They can write text to the screen.

## Methods

| Attribute | Description |
| --- | --- |
| `begin_fill(self)` | Start creating a filled shape. |
| `begin_line(self)` | Start drawing a line from the current position. |
| `circle(self, radius, extent=360)` | Draw a circle counterclockwise. |
| `dot(self, size=None, color=None)` | Draw a dot. |
| `end_fill(self)` | Complete drawing a filled shape. |
| `end_line(self)` | End the line at the current position. |
| `stamp(self)` | Stamp a copy of the sprite's image to the screen at the current position. |
| `update(self, screen=None)` | Update the sprite in preparation to draw the next frame. |
| `walk_path(self, *path, turn=True)` | Move the Sprite along a path. |
| `write(self, text, align='middle center', font='Arial', size=12, style=None, color=None)` | Write text to the screen at the turtle's current location using the pen. |

### Inherited from pygameplus.sprite.Sprite

| Attribute | Description |
| --- | --- |
| `get_direction_to(self, other)` | Return the angle that this sprite must turn toward to be pointing<br />directly at another. |
| `get_distance_to(self, other)` | Return the distance this sprite is away from another. |
| `get_touching(self, others, method='rect')` | Takes a collection of sprites and returns the subset that the sprite is<br />touching. |
| `go_to(self, x, y=None, turn=True)` | Turn the sprite and move the sprite to the given coordinates. |
| `hide(self)` | Remove the sprite from the active screen. |
| `is_touching(self, other, method='rect')` | Returns whether or not the sprite is touching another sprite (or<br />collection of sprites). |
| `is_touching_point(self, x, y=None, method='rect')` | Returns whether or not the sprite is touching a given point. |
| `move_backward(self, distance)` | Move the sprite by the given `distance` in the opposite of the<br />direction it is currently pointing. |
| `move_forward(self, distance)` | Move the sprite by the given `distance` in the direction it is currently<br />pointing. |
| `on_click(self, func, button='left', method='rect', bleeds=False)` | Add a function that will be called when the mouse is clicked on<br />this sprite. |
| `on_drag(self, func, button='left')` | Add a function that will be called when the mouse dragged while<br />clicking on this sprite. |
| `on_release(self, func, button='left')` | Add a function that will be called when the mouse is released after<br />clicking on this sprite. |
| `on_update(self, func)` | Add a custom update function that will be called on every iteration of<br />the event loop. |
| `show(self)` | Add the sprite to the active screen. |
| `turn_left(self, angle)` | Turn the sprite left (counterclockwise) by the given `angle`. |
| `turn_right(self, angle)` | Turn the sprite right (clockwise) by the given `angle`. |
| `turn_toward(self, x, y=None)` | Turn the sprite towards the given coordinates. |

### Inherited from pygame.sprite.Sprite

| Attribute | Description |
| --- | --- |
| `add(self, *groups)` | add the sprite to groups |
| `add_internal(self, group)` | For adding this sprite to a group internally. |
| `alive(self)` | does the sprite belong to any groups |
| `groups(self)` | list of Groups that contain this Sprite |
| `kill(self)` | remove the Sprite from all Groups |
| `remove(self, *groups)` | remove the sprite from groups |
| `remove_internal(self, group)` | For removing this sprite from a group internally. |

## Properties

| Attribute | Description |
| --- | --- |
| `drawing` | Whether or not the painter is currently drawing a line. |
| `fill_as_moving` | Whether or not a fill will be shown on the screen before it is complete. |
| `filling` | Whether or not the painter is currently creating a filled shape. |
| `line_width` | The current width of the lines drawn. |
| `position` | The current the position of the sprite on the screen. |
| `step_size` | The step size between points drawn on a line. |

### Inherited from pygameplus.sprite.Sprite

| Attribute | Description |
| --- | --- |
| `anchor` | The point on the image that will be placed on the sprite's position<br />and used as the center of gravity for scaling and rotation. |
| `bottom_edge` | The y-coordinate of the bottom edge of the sprite's image. |
| `bottom_edge_midpoint` | The coordinates of the midpoint of the bottom edge of the sprite's image. |
| `bottom_left_corner` | The coordinates of the bottom left corner of the sprite's image. |
| `bottom_right_corner` | The coordinates of the bottom right corner of the sprite's image. |
| `center` | The coordinates of the center of the sprite's image. |
| `center_x` | The x-coordinate of the center of the sprite's image. |
| `center_y` | The x-coordinate of the center of the sprite's image. |
| `colors` | A tuple containing the current line color and fill color. |
| `direction` | The current direction that the sprite is pointing. |
| `disabled` | Whether or not the sprite is disabled for click events. |
| `fill_color` | The current fill color. |
| `flipped` | Whether or not the original picture is flipped. |
| `flipped_horizontally` | Whether or not the original picture is flipped horizontally. |
| `flipped_vertically` | Whether or not the original picture is flipped vertically. |
| `height` | The height of the sprite's image. |
| `left_edge` | The x-coordinate of the left edge of the sprite's image. |
| `left_edge_midpoint` | The coordinates of the midpoint of the left edge of the sprite's image. |
| `line_color` | The current line color. |
| `opacity` | The opacity of the Sprite's image. |
| `picture` | The sprite's current picture. |
| `right_edge` | The x-coordinate of the right edge of the sprite's image. |
| `right_edge_midpoint` | The coordinates of the midpoint of the right edge of the sprite's image. |
| `rotates` | Whether or not the image rotates when the sprite changes direction. |
| `scale_factor` | The factor by which the image's width and height are scaled. |
| `size` | The dimensions (width and height) of the sprite's image |
| `smooth` | Whether or not the image is smoothed when scaled or rotated. |
| `tilt` | The angle that the image is tilted counterclockwise from its original<br />orientation. |
| `top_edge` | The y-coordinate of the top edge of the sprite's image. |
| `top_edge_midpoint` | The coordinates of the midpoint of the top edge of the sprite's image. |
| `top_left_corner` | The coordinates of the top left corner of the sprite's image. |
| `top_right_corner` | The coordinates of the top right corner of the sprite's image. |
| `visible` | Whether or not the sprite is visible on the active screen. |
| `width` | The width of the sprite's image. |
| `x` | The current x-coordinate of the sprite's position on the screen. |
| `y` | The current y-coordinate of the sprite's position on the screen. |

### Inherited from pygame.sprite.Sprite

| Attribute | Description |
| --- | --- |
| `layer` | Dynamic, read only property for protected _layer attribute.<br />This will get the _layer variable if it exists. |

