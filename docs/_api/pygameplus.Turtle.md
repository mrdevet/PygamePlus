---
layout: default
title: Turtle
parent: pygameplus
---
# Turtle

A Turtle is a special sprite that can move around the screen and make  drawings.  The turtle's movements will be animated so that you can see it's movements.

A turtle object includes all of the movement methods of a Sprite and the drawing methods of a Painter.

---

## Attribute Summary

### Methods

| <a href="#add">`.add(*groups)`</a> | add the sprite to groups |
| <a href="#circle">`.circle(radius, extent=360)`</a> | Draw a circle counterclockwise. |
| <a href="#dot">`.dot(size=None, color=None)`</a> | Draw a dot. |
| <a href="#end_fill">`.end_fill()`</a> | Complete drawing a filled shape. |
| <a href="#go_to">`.go_to(x, y=None, turn=True)`</a> | Turn the sprite and move the sprite to the given coordinates. |
| <a href="#hide">`.hide()`</a> | Remove the sprite from the active screen. |
| <a href="#show">`.show()`</a> | Add the sprite to the active screen. |
| <a href="#stamp">`.stamp()`</a> | Stamp a copy of the sprite's image to the screen at the current position. |
| <a href="#walk_path">`.walk_path(*path, turn=True)`</a> | Move the Sprite along a path. |
| <a href="#write">`.write(text, align='middle center', font='Arial', size=12, style=None, color=None)`</a> | Write text to the screen at the turtle's current location using the pen. |

**Inherited from <a href="../pygameplus.Painter">`pygameplus.Painter`</a>:**

- <a href="../pygameplus.Painter#begin_fill">`.begin_fill()`</a>
- <a href="../pygameplus.Painter#begin_line">`.begin_line()`</a>
- <a href="../pygameplus.Painter#end_line">`.end_line()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.update">`.update(screen=None)`</a>

**Inherited from <a href="../pygameplus.Sprite">`pygameplus.Sprite`</a>:**

- <a href="../pygameplus.Sprite#get_direction_to">`.get_direction_to(other)`</a>
- <a href="../pygameplus.Sprite#get_distance_to">`.get_distance_to(other)`</a>
- <a href="../pygameplus.Sprite#get_touching">`.get_touching(others, method='rect')`</a>
- <a href="../pygameplus.Sprite#is_touching">`.is_touching(other, method='rect')`</a>
- <a href="../pygameplus.Sprite#is_touching_point">`.is_touching_point(x, y=None, method='rect')`</a>
- <a href="../pygameplus.Sprite#move_backward">`.move_backward(distance)`</a>
- <a href="../pygameplus.Sprite#move_forward">`.move_forward(distance)`</a>
- <a href="../pygameplus.Sprite#on_click">`.on_click(func, button='left', method='rect', bleeds=False)`</a>
- <a href="../pygameplus.Sprite#on_drag">`.on_drag(func, button='left')`</a>
- <a href="../pygameplus.Sprite#on_release">`.on_release(func, button='left')`</a>
- <a href="../pygameplus.Sprite#on_update">`.on_update(func)`</a>
- <a href="../pygameplus.Sprite#turn_left">`.turn_left(angle)`</a>
- <a href="../pygameplus.Sprite#turn_right">`.turn_right(angle)`</a>
- <a href="../pygameplus.Sprite#turn_toward">`.turn_toward(x, y=None)`</a>

**Inherited from `pygame.sprite.Sprite`:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.add_internal">`.add_internal(group)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.alive">`.alive()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.groups">`.groups()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.kill">`.kill()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.remove">`.remove(*groups)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.remove_internal">`.remove_internal(group)`</a>

### Properties

| <a href="#animate">`.animate`</a> | Whether or not the turtle's movements will be animated. |
| <a href="#bottom_edge">`.bottom_edge`</a> | The y-coordinate of the bottom edge of the sprite's image. |
| <a href="#bottom_edge_midpoint">`.bottom_edge_midpoint`</a> | The coordinates of the midpoint of the bottom edge of the sprite's image. |
| <a href="#bottom_left_corner">`.bottom_left_corner`</a> | The coordinates of the bottom left corner of the sprite's image. |
| <a href="#bottom_right_corner">`.bottom_right_corner`</a> | The coordinates of the bottom right corner of the sprite's image. |
| <a href="#center_x">`.center_x`</a> | The x-coordinate of the center of the sprite's image. |
| <a href="#center_y">`.center_y`</a> | The x-coordinate of the center of the sprite's image. |
| <a href="#colors">`.colors`</a> | A tuple containing the current line color and fill color. |
| <a href="#direction">`.direction`</a> | The current direction that the sprite is pointing. |
| <a href="#fill_as_moving">`.fill_as_moving`</a> | Whether or not a fill will be shown on the screen before it is complete. |
| <a href="#frame_rate">`.frame_rate`</a> | The number of animation frames per second. |
| <a href="#height">`.height`</a> | The height of the sprite's image. |
| <a href="#left_edge">`.left_edge`</a> | The x-coordinate of the left edge of the sprite's image. |
| <a href="#left_edge_midpoint">`.left_edge_midpoint`</a> | The coordinates of the midpoint of the left edge of the sprite's image. |
| <a href="#position">`.position`</a> | The current the position of the sprite on the screen. |
| <a href="#right_edge">`.right_edge`</a> | The x-coordinate of the right edge of the sprite's image. |
| <a href="#right_edge_midpoint">`.right_edge_midpoint`</a> | The coordinates of the midpoint of the right edge of the sprite's image. |
| <a href="#rotates">`.rotates`</a> | Whether or not the image rotates when the sprite changes direction. |
| <a href="#scale_factor">`.scale_factor`</a> | The factor by which the image's width and height are scaled. |
| <a href="#smooth">`.smooth`</a> | Whether or not the image is smoothed when scaled or rotated. |
| <a href="#speed">`.speed`</a> | The current speed (in pixels per second) that the turtle moves on  the screen. |
| <a href="#tilt">`.tilt`</a> | The angle that the image is tilted counterclockwise from its original orientation. |
| <a href="#top_edge">`.top_edge`</a> | The y-coordinate of the top edge of the sprite's image. |
| <a href="#top_edge_midpoint">`.top_edge_midpoint`</a> | The coordinates of the midpoint of the top edge of the sprite's image. |
| <a href="#top_left_corner">`.top_left_corner`</a> | The coordinates of the top left corner of the sprite's image. |
| <a href="#top_right_corner">`.top_right_corner`</a> | The coordinates of the top right corner of the sprite's image. |
| <a href="#visible">`.visible`</a> | Whether or not the sprite is visible on the active screen. |
| <a href="#width">`.width`</a> | The width of the sprite's image. |
| <a href="#x">`.x`</a> | The current x-coordinate of the sprite's position on the screen. |
| <a href="#y">`.y`</a> | The current y-coordinate of the sprite's position on the screen. |

**Inherited from <a href="../pygameplus.Painter">`pygameplus.Painter`</a>:**

- <a href="../pygameplus.Painter#drawing">`.drawing`</a>
- <a href="../pygameplus.Painter#filling">`.filling`</a>
- <a href="../pygameplus.Painter#line_width">`.line_width`</a>
- <a href="../pygameplus.Painter#step_size">`.step_size`</a>

**Inherited from <a href="../pygameplus.Sprite">`pygameplus.Sprite`</a>:**

- <a href="../pygameplus.Sprite#anchor">`.anchor`</a>
- <a href="../pygameplus.Sprite#center">`.center`</a>
- <a href="../pygameplus.Sprite#disabled">`.disabled`</a>
- <a href="../pygameplus.Sprite#fill_color">`.fill_color`</a>
- <a href="../pygameplus.Sprite#flipped">`.flipped`</a>
- <a href="../pygameplus.Sprite#flipped_horizontally">`.flipped_horizontally`</a>
- <a href="../pygameplus.Sprite#flipped_vertically">`.flipped_vertically`</a>
- <a href="../pygameplus.Sprite#line_color">`.line_color`</a>
- <a href="../pygameplus.Sprite#opacity">`.opacity`</a>
- <a href="../pygameplus.Sprite#picture">`.picture`</a>
- <a href="../pygameplus.Sprite#size">`.size`</a>

**Inherited from `pygame.sprite.Sprite`:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.layer">`.layer`</a>

---

## Attribute Details

### `.add(*groups)` {#add}

> add the sprite to groups
> 
> Sprite.add(*groups): return None
> 
> Any number of Group instances can be passed as arguments. The Sprite will be added to the Groups it is not already a member of.

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

### `.go_to(x, y=None, turn=True)` {#go_to}

> Turn the sprite and move the sprite to the given coordinates.
> 
> Unlike changing the position property, this method will also turn the sprite in the direction of the given location.  This behaviour can be turned off by setting the `turn` argument to `False`.

### `.hide()` {#hide}

> Remove the sprite from the active screen.

### `.show()` {#show}

> Add the sprite to the active screen.

### `.stamp()` {#stamp}

> Stamp a copy of the sprite's image to the screen at the current position.

### `.walk_path(*path, turn=True)` {#walk_path}

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

### `.animate` {#animate}

> Whether or not the turtle's movements will be animated.
> 
> If set to False, movements will happen instantaneously.

### `.bottom_edge` {#bottom_edge}

> The y-coordinate of the bottom edge of the sprite's image.

### `.bottom_edge_midpoint` {#bottom_edge_midpoint}

> The coordinates of the midpoint of the bottom edge of the sprite's image.

### `.bottom_left_corner` {#bottom_left_corner}

> The coordinates of the bottom left corner of the sprite's image.

### `.bottom_right_corner` {#bottom_right_corner}

> The coordinates of the bottom right corner of the sprite's image.

### `.center_x` {#center_x}

> The x-coordinate of the center of the sprite's image.

### `.center_y` {#center_y}

> The x-coordinate of the center of the sprite's image.

### `.colors` {#colors}

> A tuple containing the current line color and fill color.
> 
> You can change both the line color and fill color by setting this property to be a 2-tuple containing each respective color.  You can change both the line color and fill color to the same color by providing one color.

### `.direction` {#direction}

> The current direction that the sprite is pointing.
> 
> The direction is an angle (in degrees) counterclockwise from the positive x-axis.  Here are some important directions:  - 0 degrees is directly to the right  - 90 degrees is directly up  - 180 degrees is directly to the left  - 270 degrees is directly down

### `.fill_as_moving` {#fill_as_moving}

> Whether or not a fill will be shown on the screen before it is complete.

### `.frame_rate` {#frame_rate}

> The number of animation frames per second.

### `.height` {#height}

> The height of the sprite's image.

### `.left_edge` {#left_edge}

> The x-coordinate of the left edge of the sprite's image.

### `.left_edge_midpoint` {#left_edge_midpoint}

> The coordinates of the midpoint of the left edge of the sprite's image.

### `.position` {#position}

> The current the position of the sprite on the screen.
> 
> The position is a pair of coordinates (x and y) which represent the distance that the sprite is from the center of the screen.  That is, the center of the screen is (0, 0) and the x-coordinate and y-coordinate represent respectively how far horizontally and vertically the sprite is from there.  Think of the screen as the traditional 2D coordinate plane used in mathematics.

### `.right_edge` {#right_edge}

> The x-coordinate of the right edge of the sprite's image.

### `.right_edge_midpoint` {#right_edge_midpoint}

> The coordinates of the midpoint of the right edge of the sprite's image.

### `.rotates` {#rotates}

> Whether or not the image rotates when the sprite changes direction.

### `.scale_factor` {#scale_factor}

> The factor by which the image's width and height are scaled.
> 
> If the factor is greater than 1, then the image is enlarged by multiplying its original dimension by that number.  If factor is less than 1, then the image is shrunk by multiplying its original dimension by that number.  If factor equals 1, then the image is scaled to its original size.

### `.smooth` {#smooth}

> Whether or not the image is smoothed when scaled or rotated.
> 
> By default, a quick and simple scale and rotation is applied.  This can cause images to be pixelated (when enlarged), loose detail (when shrunk), or be distorted (when rotating).  If you set `smooth` to be `True`, then each new pixel will be sampled and an average color will be used.  This makes to scaled and rotated images be more smooth, but takes longer.  You may want to avoid smooth scaling if you will be scaling or rotating the image very frequently.

### `.speed` {#speed}

> The current speed (in pixels per second) that the turtle moves on  the screen.

### `.tilt` {#tilt}

> The angle that the image is tilted counterclockwise from its original orientation.
> 
> If image rotation is off, then the image will stay tilted at this angle no matter what direction the sprite is pointing.  If image rotation is on, then the image will stay tilted at this angle relative to the sprite's direction.

### `.top_edge` {#top_edge}

> The y-coordinate of the top edge of the sprite's image.

### `.top_edge_midpoint` {#top_edge_midpoint}

> The coordinates of the midpoint of the top edge of the sprite's image.

### `.top_left_corner` {#top_left_corner}

> The coordinates of the top left corner of the sprite's image.

### `.top_right_corner` {#top_right_corner}

> The coordinates of the top right corner of the sprite's image.

### `.visible` {#visible}

> Whether or not the sprite is visible on the active screen.

### `.width` {#width}

> The width of the sprite's image.

### `.x` {#x}

> The current x-coordinate of the sprite's position on the screen.

### `.y` {#y}

> The current y-coordinate of the sprite's position on the screen.

