---
layout: default
title: Painter
parent: pygameplus
---
# Painter

A Painter is a special sub-class of a Sprite with extra methods used to 
draw on the screen.  All methods of a Sprite object can be used on
Painter objects.

Some features of Painter objects include:
 - They can draw on the screen when they move.
 - They can be used to draw filled polygons.
 - They can draw dots and circles.
 - They can stamp copies of their image to the screen.
 - They can write text to the screen.

---

## Attribute Summary

### Methods

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

**Inherited from `pygameplus.sprite.Sprite`:**

- `get_direction_to(self, other)`
- `get_distance_to(self, other)`
- `get_touching(self, others, method='rect')`
- `go_to(self, x, y=None, turn=True)`
- `hide(self)`
- `is_touching(self, other, method='rect')`
- `is_touching_point(self, x, y=None, method='rect')`
- `move_backward(self, distance)`
- `move_forward(self, distance)`
- `on_click(self, func, button='left', method='rect', bleeds=False)`
- `on_drag(self, func, button='left')`
- `on_release(self, func, button='left')`
- `on_update(self, func)`
- `show(self)`
- `turn_left(self, angle)`
- `turn_right(self, angle)`
- `turn_toward(self, x, y=None)`

**Inherited from `pygame.sprite.Sprite`:**

- `add(self, *groups)`
- `add_internal(self, group)`
- `alive(self)`
- `groups(self)`
- `kill(self)`
- `remove(self, *groups)`
- `remove_internal(self, group)`

### Properties

| Attribute | Description |
| --- | --- |
| `drawing` | Whether or not the painter is currently drawing a line. |
| `fill_as_moving` | Whether or not a fill will be shown on the screen before it is complete. |
| `filling` | Whether or not the painter is currently creating a filled shape. |
| `line_width` | The current width of the lines drawn. |
| `position` | The current the position of the sprite on the screen. |
| `step_size` | The step size between points drawn on a line. |

**Inherited from `pygameplus.sprite.Sprite`:**

- `anchor`
- `bottom_edge`
- `bottom_edge_midpoint`
- `bottom_left_corner`
- `bottom_right_corner`
- `center`
- `center_x`
- `center_y`
- `colors`
- `direction`
- `disabled`
- `fill_color`
- `flipped`
- `flipped_horizontally`
- `flipped_vertically`
- `height`
- `left_edge`
- `left_edge_midpoint`
- `line_color`
- `opacity`
- `picture`
- `right_edge`
- `right_edge_midpoint`
- `rotates`
- `scale_factor`
- `size`
- `smooth`
- `tilt`
- `top_edge`
- `top_edge_midpoint`
- `top_left_corner`
- `top_right_corner`
- `visible`
- `width`
- `x`
- `y`

**Inherited from `pygame.sprite.Sprite`:**

- `layer`

---

## Attribute Details

### `begin_fill(self)`

> Start creating a filled shape.
> 
> This function must be followed with a call to end_fill() which
will draw the filled shape using all of the points visited
from the call of this method.
> 
> If `as_moving` is set to `True`, then the filled shape will be redrawn
after each move of the sprite.

### `begin_line(self)`

> Start drawing a line from the current position.

### `circle(self, radius, extent=360)`

> Draw a circle counterclockwise.
> 
> The circle will have the given `radius`.  If `radius` is negative, then
the circle is draw clockwise.
> 
> The `extent` is used to draw an arc around a portion of a circle.  If 
`extent` is negative, draw the circle clockwise.
> 
> The circle will actually be an approximation.  The turtle will really
draw a regular polygon with 360 sides.

### `dot(self, size=None, color=None)`

> Draw a dot.
> 
> The dot will be centered at the current position and have diameter
`size`.  If no size is given a dot slightly larger than the line width
will be drawn.
> 
> If the `color` is not specified, the line color is used.

### `drawing`

> Whether or not the painter is currently drawing a line.

### `end_fill(self)`

> Complete drawing a filled shape.
> 
> This function must be preceded by a call to begin_fill().  When
this method is called, a filled shape will be drawn using all of the
points visited since begin_fill() was called.

### `end_line(self)`

> End the line at the current position.

### `fill_as_moving`

> Whether or not a fill will be shown on the screen before it is complete.

### `filling`

> Whether or not the painter is currently creating a filled shape.

### `line_width`

> The current width of the lines drawn.

### `position`

> The current the position of the sprite on the screen.
> 
> The position is a pair of coordinates (x and y) which represent the
distance that the sprite is from the center of the screen.  That is,
the center of the screen is (0, 0) and the x-coordinate and y-coordinate
represent respectively how far horizontally and vertically the sprite is
from there.  Think of the screen as the traditional 2D coordinate plane
used in mathematics.

### `stamp(self)`

> Stamp a copy of the sprite's image to the screen at the current position.

### `step_size`

> The step size between points drawn on a line.

### `update(self, screen=None)`

> Update the sprite in preparation to draw the next frame.
> 
> This method should generally not be called explicitly, but will be called
by the event loop if the sprite is on the active screen.

### `walk_path(self, *path, turn=True)`

> Move the Sprite along a path.
> 
> If a line is currently being drawn, then it will continue from the 
current position and be drawn along the path.
> 
> The path should be a list of coordinate pairs
(e.g. `[(100, 0), (-200, 100), (200, -50)]`)
> 
> By default, this method will also turn the turtle in the direction 
of each of the given positions.  This behaviour can be turned of by
setting the `turn` argument to `False`.

### `write(self, text, align='middle center', font='Arial', size=12, style=None, color=None)`

> Write text to the screen at the turtle's current location using the pen.
> 
> The `align` parameter sets where the turtle aligns with the text being
written.  It is a string containing "left", "right", "center", "top",
"bottom", "middle" or a combination separated by space (e.g. 
"bottom center")
> 
> The `font` parameter can be the name of a font on the system or a
True Type Font file (.ttf) located in the directory.
> 
> The `size` is the height of the text in pixels.
> 
> The `style` argument can be "bold", "italic", "underline" or a 
combination separated by space (e.g. "bold italic").
> 
> If the `color` is not specified, the line color is used.

