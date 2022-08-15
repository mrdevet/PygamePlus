---
layout: default
title: Turtle
parent: pygameplus
---
# Turtle

A Turtle is a special sprite that can move around the screen and make  drawings.  When you move the turtle using any of its methods, it will be automatically animated.

A turtle object includes all of the movement methods of a Sprite  and the drawing methods of a Painter.

---

## Attribute Summary

### Methods

| <a href="#go_to">`.go_to(x, y=None, turn=True, reverse=False)`</a> | Turn the sprite and move the sprite to the given coordinates. |
| <a href="#turn_to">`.turn_to(direction, reverse=False)`</a> | Turn the sprite to the point at the given `direction`. |
| <a href="#update">`.update(screen=None)`</a> | Update the sprite in preparation to draw the next frame. |

**Inherited from <a href="../pygameplus.Painter">`pygameplus.Painter`</a>:**

- <a href="../pygameplus.Painter#begin_fill">`.begin_fill()`</a>
- <a href="../pygameplus.Painter#begin_line">`.begin_line()`</a>
- <a href="../pygameplus.Painter#circle">`.circle(radius, extent=360)`</a>
- <a href="../pygameplus.Painter#dot">`.dot(size=None, color=None)`</a>
- <a href="../pygameplus.Painter#end_fill">`.end_fill()`</a>
- <a href="../pygameplus.Painter#end_line">`.end_line()`</a>
- <a href="../pygameplus.Painter#stamp">`.stamp()`</a>
- <a href="../pygameplus.Painter#walk_path">`.walk_path(*path, turn=True, reverse=False)`</a>
- <a href="../pygameplus.Painter#write">`.write(text, align='middle center', font='Arial', size=12, style=None, color=None)`</a>

**Inherited from <a href="../pygameplus.Sprite">`pygameplus.Sprite`</a>:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.add_internal">`.add_internal(group)`</a>
- <a href="../pygameplus.Sprite#get_direction_to">`.get_direction_to(other)`</a>
- <a href="../pygameplus.Sprite#get_distance_to">`.get_distance_to(other)`</a>
- <a href="../pygameplus.Sprite#get_touching">`.get_touching(others, method='rect')`</a>
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
- <a href="../pygameplus.Sprite#turn_toward">`.turn_toward(x, y=None, reverse=False)`</a>

**Inherited from `pygame.sprite.Sprite`:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.add">`.add(*groups)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.alive">`.alive()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.groups">`.groups()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.kill">`.kill()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.remove">`.remove(*groups)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.remove_internal">`.remove_internal(group)`</a>

### Properties

| <a href="#animate">`.animate`</a> | Whether or not the turtle's movements will be animated. |
| <a href="#speed">`.speed`</a> | The current speed (in pixels per second) that the turtle moves on  the screen. |

**Inherited from <a href="../pygameplus.Painter">`pygameplus.Painter`</a>:**

- <a href="../pygameplus.Painter#drawing">`.drawing`</a>
- <a href="../pygameplus.Painter#fill_as_moving">`.fill_as_moving`</a>
- <a href="../pygameplus.Painter#filling">`.filling`</a>
- <a href="../pygameplus.Painter#line_width">`.line_width`</a>
- <a href="../pygameplus.Painter#position">`.position`</a>
- <a href="../pygameplus.Painter#step_size">`.step_size`</a>

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

### `.go_to(x, y=None, turn=True, reverse=False)` {#go_to}

> Turn the sprite and move the sprite to the given coordinates.
> 
> Unlike changing the position property, this method will also turn the sprite in the direction of the given location.  This behaviour can be turned off by setting the `turn` argument to `False`.

### `.turn_to(direction, reverse=False)` {#turn_to}

> Turn the sprite to the point at the given `direction`.
> 
> The direction is an angle (in degrees) counterclockwise from the positive x-axis.  Here are some important directions:  - 0 degrees is directly to the right  - 90 degrees is directly up  - 180 degrees is directly to the left  - 270 degrees is directly down  

### `.update(screen=None)` {#update}

> Update the sprite in preparation to draw the next frame.
> 
> This method should generally not be called explicitly, but will be called by the event loop if the sprite is on the active screen.

### `.animate` {#animate}

> Whether or not the turtle's movements will be animated.
> 
> If set to False, movements will happen instantaneously.

### `.speed` {#speed}

> The current speed (in pixels per second) that the turtle moves on  the screen.

