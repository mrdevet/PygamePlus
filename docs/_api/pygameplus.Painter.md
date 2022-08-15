---
layout: default
title: Painter
parent: pygameplus
---
# Painter

A Painter is a special sub-class of a Sprite with extra methods used to  draw on the screen.  All methods of a Sprite object can be used on Painter objects.

Some features of Painter objects include:  - They can draw on the screen when they move.  - They can be used to draw filled polygons.  - They can draw dots and circles.  - They can stamp copies of their image to the screen.  - They can write text to the screen.

---

## Attribute Summary

### Methods

| <a href="#begin_fill">`.begin_fill()`</a> | Start creating a filled shape. |
| <a href="#begin_line">`.begin_line()`</a> | Start drawing a line from the current position. |
| <a href="#circle">`.circle(radius, extent=360)`</a> | Draw a circle counterclockwise. |
| <a href="#dot">`.dot(size=None, color=None)`</a> | Draw a dot. |
| <a href="#end_fill">`.end_fill()`</a> | Complete drawing a filled shape. |
| <a href="#end_line">`.end_line()`</a> | End the line at the current position. |
| <a href="#stamp">`.stamp()`</a> | Stamp a copy of the sprite's image to the screen at the current position. |
| <a href="#update">`.update(screen=None)`</a> | Update the sprite in preparation to draw the next frame. |
| <a href="#walk_path">`.walk_path(*path, turn=True, reverse=False)`</a> | Move the Sprite along a path. |
| <a href="#write">`.write(text, align='middle center', font='Arial', size=12, style=None, color=None)`</a> | Write text to the screen at the turtle's current location using the pen. |

**Inherited from <a href="../pygameplus.Sprite">`pygameplus.Sprite`</a>:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.add_internal">`.add_internal(group)`</a>
- <a href="../pygameplus.Sprite#get_direction_to">`.get_direction_to(other)`</a>
- <a href="../pygameplus.Sprite#get_distance_to">`.get_distance_to(other)`</a>
- <a href="../pygameplus.Sprite#get_touching">`.get_touching(others, method='rect')`</a>
- <a href="../pygameplus.Sprite#go_to">`.go_to(x, y=None, turn=True, reverse=False)`</a>
- <a href="../pygameplus.Sprite#hide">`.hide()`</a>
- <a href="../pygameplus.Sprite#is_touching">`.is_touching(other, method='rect')`</a>
- <a href="../pygameplus.Sprite#is_touching_point">`.is_touching_point(x, y=None, method='rect')`</a>
- <a href="../pygameplus.Sprite#move_backward">`.move_backward(distance)`</a>
- <a href="../pygameplus.Sprite#move_forward">`.move_forward(distance)`</a>
- <a href="../pygameplus.Sprite#on_click">`.on_click(func, button='left', method='rect', bleeds=False)`</a>
- <a href="../pygameplus.Sprite#on_drag">`.on_drag(func, button='left')`</a>
- <a href="../pygameplus.Sprite#on_release">`.on_release(func, button='left')`</a>
- <a href="../pygameplus.Sprite#on_update">`.on_update(func)`</a>
- <a href="../pygameplus.Sprite#show">`.show()`</a>
- <a href="../pygameplus.Sprite#turn_left">`.turn_left(angle)`</a>
- <a href="../pygameplus.Sprite#turn_right">`.turn_right(angle)`</a>
- <a href="../pygameplus.Sprite#turn_to">`.turn_to(direction, reverse=False)`</a>
- <a href="../pygameplus.Sprite#turn_toward">`.turn_toward(x, y=None, reverse=False)`</a>

**Inherited from `pygame.sprite.Sprite`:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.add">`.add(*groups)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.alive">`.alive()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.groups">`.groups()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.kill">`.kill()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.remove">`.remove(*groups)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.remove_internal">`.remove_internal(group)`</a>

### Properties

| <a href="#drawing">`.drawing`</a> | Whether or not the painter is currently drawing a line. |
| <a href="#fill_as_moving">`.fill_as_moving`</a> | Whether or not a fill will be shown on the screen before it is complete. |
| <a href="#filling">`.filling`</a> | Whether or not the painter is currently creating a filled shape. |
| <a href="#line_width">`.line_width`</a> | The current width of the lines drawn. |
| <a href="#position">`.position`</a> | The current the position of the sprite on the screen. |
| <a href="#step_size">`.step_size`</a> | The step size between points drawn on a line. |

**Inherited from <a href="../pygameplus.Sprite">`pygameplus.Sprite`</a>:**

- <a href="../pygameplus.Sprite#anchor">`.anchor`</a>
- <a href="../pygameplus.Sprite#bottom_edge">`.bottom_edge`</a>
- <a href="../pygameplus.Sprite#bottom_edge_midpoint">`.bottom_edge_midpoint`</a>
- <a href="../pygameplus.Sprite#bottom_left_corner">`.bottom_left_corner`</a>
- <a href="../pygameplus.Sprite#bottom_right_corner">`.bottom_right_corner`</a>
- <a href="../pygameplus.Sprite#center">`.center`</a>
- <a href="../pygameplus.Sprite#center_x">`.center_x`</a>
- <a href="../pygameplus.Sprite#center_y">`.center_y`</a>
- <a href="../pygameplus.Sprite#colors">`.colors`</a>
- <a href="../pygameplus.Sprite#direction">`.direction`</a>
- <a href="../pygameplus.Sprite#disabled">`.disabled`</a>
- <a href="../pygameplus.Sprite#fill_color">`.fill_color`</a>
- <a href="../pygameplus.Sprite#flipped">`.flipped`</a>
- <a href="../pygameplus.Sprite#flipped_horizontally">`.flipped_horizontally`</a>
- <a href="../pygameplus.Sprite#flipped_vertically">`.flipped_vertically`</a>
- <a href="../pygameplus.Sprite#height">`.height`</a>
- <a href="../pygameplus.Sprite#left_edge">`.left_edge`</a>
- <a href="../pygameplus.Sprite#left_edge_midpoint">`.left_edge_midpoint`</a>
- <a href="../pygameplus.Sprite#line_color">`.line_color`</a>
- <a href="../pygameplus.Sprite#opacity">`.opacity`</a>
- <a href="../pygameplus.Sprite#picture">`.picture`</a>
- <a href="../pygameplus.Sprite#right_edge">`.right_edge`</a>
- <a href="../pygameplus.Sprite#right_edge_midpoint">`.right_edge_midpoint`</a>
- <a href="../pygameplus.Sprite#rotates">`.rotates`</a>
- <a href="../pygameplus.Sprite#scale_factor">`.scale_factor`</a>
- <a href="../pygameplus.Sprite#size">`.size`</a>
- <a href="../pygameplus.Sprite#smooth">`.smooth`</a>
- <a href="../pygameplus.Sprite#tilt">`.tilt`</a>
- <a href="../pygameplus.Sprite#top_edge">`.top_edge`</a>
- <a href="../pygameplus.Sprite#top_edge_midpoint">`.top_edge_midpoint`</a>
- <a href="../pygameplus.Sprite#top_left_corner">`.top_left_corner`</a>
- <a href="../pygameplus.Sprite#top_right_corner">`.top_right_corner`</a>
- <a href="../pygameplus.Sprite#visible">`.visible`</a>
- <a href="../pygameplus.Sprite#width">`.width`</a>
- <a href="../pygameplus.Sprite#x">`.x`</a>
- <a href="../pygameplus.Sprite#y">`.y`</a>

**Inherited from `pygame.sprite.Sprite`:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.layer">`.layer`</a>

---

## Attribute Details

### `.begin_fill()` {#begin_fill}

> Start creating a filled shape.
> 
> This function must be followed with a call to end_fill() which will draw the filled shape using all of the points visited from the call of this method.
> 
> If `as_moving` is set to `True`, then the filled shape will be redrawn after each move of the sprite.

### `.begin_line()` {#begin_line}

> Start drawing a line from the current position.

### `.circle(radius, extent=360)` {#circle}

> Draw a circle counterclockwise.
> 
> The circle will have the given `radius`.  If `radius` is negative, then the circle is draw clockwise.
> 
> The `extent` is used to draw an arc around a portion of a circle.  If  `extent` is negative, draw the circle clockwise.
> 
> The circle will actually be an approximation.  The turtle will really draw a regular polygon with 360 sides.

### `.dot(size=None, color=None)` {#dot}

> Draw a dot.
> 
> The dot will be centered at the current position and have diameter `size`.  If no size is given a dot slightly larger than the line width will be drawn.
> 
> If the `color` is not specified, the line color is used.

### `.end_fill()` {#end_fill}

> Complete drawing a filled shape.
> 
> This function must be preceded by a call to begin_fill().  When this method is called, a filled shape will be drawn using all of the points visited since begin_fill() was called.

### `.end_line()` {#end_line}

> End the line at the current position.

### `.stamp()` {#stamp}

> Stamp a copy of the sprite's image to the screen at the current position.

### `.update(screen=None)` {#update}

> Update the sprite in preparation to draw the next frame.
> 
> This method should generally not be called explicitly, but will be called by the event loop if the sprite is on the active screen.

### `.walk_path(*path, turn=True, reverse=False)` {#walk_path}

> Move the Sprite along a path.
> 
> If a line is currently being drawn, then it will continue from the  current position and be drawn along the path.
> 
> The path should be a list of coordinate pairs (e.g. `[(100, 0), (-200, 100), (200, -50)]`)
> 
> By default, this method will also turn the turtle in the direction  of each of the given positions.  This behaviour can be turned of by setting the `turn` argument to `False`.

### `.write(text, align='middle center', font='Arial', size=12, style=None, color=None)` {#write}

> Write text to the screen at the turtle's current location using the pen.
> 
> The `align` parameter sets where the turtle aligns with the text being written.  It is a string containing "left", "right", "center", "top", "bottom", "middle" or a combination separated by space (e.g.  "bottom center")
> 
> The `font` parameter can be the name of a font on the system or a True Type Font file (.ttf) located in the directory.
> 
> The `size` is the height of the text in pixels.
> 
> The `style` argument can be "bold", "italic", "underline" or a  combination separated by space (e.g. "bold italic").
> 
> If the `color` is not specified, the line color is used.

### `.drawing` {#drawing}

> Whether or not the painter is currently drawing a line.

### `.fill_as_moving` {#fill_as_moving}

> Whether or not a fill will be shown on the screen before it is complete.

### `.filling` {#filling}

> Whether or not the painter is currently creating a filled shape.

### `.line_width` {#line_width}

> The current width of the lines drawn.

### `.position` {#position}

> The current the position of the sprite on the screen.
> 
> The position is a pair of coordinates (x and y) which represent the distance that the sprite is from the center of the screen.  That is, the center of the screen is (0, 0) and the x-coordinate and y-coordinate represent respectively how far horizontally and vertically the sprite is from there.  Think of the screen as the traditional 2D coordinate plane used in mathematics.

### `.step_size` {#step_size}

> The step size between points drawn on a line.

