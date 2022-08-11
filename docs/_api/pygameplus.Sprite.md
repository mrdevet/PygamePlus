---
layout: default
title: Sprite
parent: pygameplus
---
# Sprite

A Sprite represents an image that moves around the screen in a game.

Sprite objects store the following information necessary for drawing these images on the screen:  - The position of the sprite on the screen using coordinates  - The direction that the sprite is pointing using an angle measured    counterclockwise from the positive x-axis.

Methods are provided for the following:  - Moving and turning the sprite  - Detecting whether or not a sprite is touching other sprites  - Animating the sprite  - Adding behaviour when the mouse interacts with the sprite

---

## Attribute Summary

### Methods

| <a href="#get_direction_to">`.get_direction_to(other)`</a> | Return the angle that this sprite must turn toward to be pointing directly at another. |
| <a href="#get_distance_to">`.get_distance_to(other)`</a> | Return the distance this sprite is away from another. |
| <a href="#get_touching">`.get_touching(others, method='rect')`</a> | Takes a collection of sprites and returns the subset that the sprite is touching. |
| <a href="#go_to">`.go_to(x, y=None, turn=True)`</a> | Turn the sprite and move the sprite to the given coordinates. |
| <a href="#hide">`.hide()`</a> | Remove the sprite from the active screen. |
| <a href="#is_touching">`.is_touching(other, method='rect')`</a> | Returns whether or not the sprite is touching another sprite (or collection of sprites). |
| <a href="#is_touching_point">`.is_touching_point(x, y=None, method='rect')`</a> | Returns whether or not the sprite is touching a given point. |
| <a href="#move_backward">`.move_backward(distance)`</a> | Move the sprite by the given `distance` in the opposite of the direction it is currently pointing. |
| <a href="#move_forward">`.move_forward(distance)`</a> | Move the sprite by the given `distance` in the direction it is currently pointing. |
| <a href="#on_click">`.on_click(func, button='left', method='rect', bleeds=False)`</a> | Add a function that will be called when the mouse is clicked on this sprite. |
| <a href="#on_drag">`.on_drag(func, button='left')`</a> | Add a function that will be called when the mouse dragged while clicking on this sprite. |
| <a href="#on_release">`.on_release(func, button='left')`</a> | Add a function that will be called when the mouse is released after clicking on this sprite. |
| <a href="#on_update">`.on_update(func)`</a> | Add a custom update function that will be called on every iteration of the event loop. |
| <a href="#show">`.show()`</a> | Add the sprite to the active screen. |
| <a href="#turn_left">`.turn_left(angle)`</a> | Turn the sprite left (counterclockwise) by the given `angle`. |
| <a href="#turn_right">`.turn_right(angle)`</a> | Turn the sprite right (clockwise) by the given `angle`. |
| <a href="#turn_toward">`.turn_toward(x, y=None)`</a> | Turn the sprite towards the given coordinates. |
| <a href="#update">`.update(screen=None)`</a> | Update the sprite in preparation to draw the next frame. |

**Inherited from `pygame.sprite.Sprite`:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.add">`.add(*groups)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.add_internal">`.add_internal(group)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.alive">`.alive()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.groups">`.groups()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.kill">`.kill()`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.remove">`.remove(*groups)`</a>
- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.remove_internal">`.remove_internal(group)`</a>

### Properties

| <a href="#anchor">`.anchor`</a> | The point on the image that will be placed on the sprite's position and used as the center of gravity for scaling and rotation. |
| <a href="#bottom_edge">`.bottom_edge`</a> | The y-coordinate of the bottom edge of the sprite's image. |
| <a href="#bottom_edge_midpoint">`.bottom_edge_midpoint`</a> | The coordinates of the midpoint of the bottom edge of the sprite's image. |
| <a href="#bottom_left_corner">`.bottom_left_corner`</a> | The coordinates of the bottom left corner of the sprite's image. |
| <a href="#bottom_right_corner">`.bottom_right_corner`</a> | The coordinates of the bottom right corner of the sprite's image. |
| <a href="#center">`.center`</a> | The coordinates of the center of the sprite's image. |
| <a href="#center_x">`.center_x`</a> | The x-coordinate of the center of the sprite's image. |
| <a href="#center_y">`.center_y`</a> | The x-coordinate of the center of the sprite's image. |
| <a href="#colors">`.colors`</a> | A tuple containing the current line color and fill color. |
| <a href="#direction">`.direction`</a> | The current direction that the sprite is pointing. |
| <a href="#disabled">`.disabled`</a> | Whether or not the sprite is disabled for click events. |
| <a href="#fill_color">`.fill_color`</a> | The current fill color. |
| <a href="#flipped">`.flipped`</a> | Whether or not the original picture is flipped. |
| <a href="#flipped_horizontally">`.flipped_horizontally`</a> | Whether or not the original picture is flipped horizontally. |
| <a href="#flipped_vertically">`.flipped_vertically`</a> | Whether or not the original picture is flipped vertically. |
| <a href="#height">`.height`</a> | The height of the sprite's image. |
| <a href="#left_edge">`.left_edge`</a> | The x-coordinate of the left edge of the sprite's image. |
| <a href="#left_edge_midpoint">`.left_edge_midpoint`</a> | The coordinates of the midpoint of the left edge of the sprite's image. |
| <a href="#line_color">`.line_color`</a> | The current line color. |
| <a href="#opacity">`.opacity`</a> | The opacity of the Sprite's image. |
| <a href="#picture">`.picture`</a> | The sprite's current picture. |
| <a href="#position">`.position`</a> | The current the position of the sprite on the screen. |
| <a href="#right_edge">`.right_edge`</a> | The x-coordinate of the right edge of the sprite's image. |
| <a href="#right_edge_midpoint">`.right_edge_midpoint`</a> | The coordinates of the midpoint of the right edge of the sprite's image. |
| <a href="#rotates">`.rotates`</a> | Whether or not the image rotates when the sprite changes direction. |
| <a href="#scale_factor">`.scale_factor`</a> | The factor by which the image's width and height are scaled. |
| <a href="#size">`.size`</a> | The dimensions (width and height) of the sprite's image |
| <a href="#smooth">`.smooth`</a> | Whether or not the image is smoothed when scaled or rotated. |
| <a href="#tilt">`.tilt`</a> | The angle that the image is tilted counterclockwise from its original orientation. |
| <a href="#top_edge">`.top_edge`</a> | The y-coordinate of the top edge of the sprite's image. |
| <a href="#top_edge_midpoint">`.top_edge_midpoint`</a> | The coordinates of the midpoint of the top edge of the sprite's image. |
| <a href="#top_left_corner">`.top_left_corner`</a> | The coordinates of the top left corner of the sprite's image. |
| <a href="#top_right_corner">`.top_right_corner`</a> | The coordinates of the top right corner of the sprite's image. |
| <a href="#visible">`.visible`</a> | Whether or not the sprite is visible on the active screen. |
| <a href="#width">`.width`</a> | The width of the sprite's image. |
| <a href="#x">`.x`</a> | The current x-coordinate of the sprite's position on the screen. |
| <a href="#y">`.y`</a> | The current y-coordinate of the sprite's position on the screen. |

**Inherited from `pygame.sprite.Sprite`:**

- <a href="https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite.layer">`.layer`</a>

---

## Attribute Details

### `.get_direction_to(other)` {#get_direction_to}

> Return the angle that this sprite must turn toward to be pointing directly at another.

### `.get_distance_to(other)` {#get_distance_to}

> Return the distance this sprite is away from another.

### `.get_touching(others, method='rect')` {#get_touching}

> Takes a collection of sprites and returns the subset that the sprite is touching.
> 
> See the Sprite.is_touching() method for details on the `method` parameter.

### `.go_to(x, y=None, turn=True)` {#go_to}

> Turn the sprite and move the sprite to the given coordinates.
> 
> Unlike changing the position property, this method will also turn the sprite in the direction of the given location.  This behaviour can be turned off by setting the `turn` argument to `False`.

### `.hide()` {#hide}

> Remove the sprite from the active screen.

### `.is_touching(other, method='rect')` {#is_touching}

> Returns whether or not the sprite is touching another sprite (or collection of sprites).
> 
> The `method` argument can be used to specify which type of collision detection to use:  - The "rect" method will determine if the rectangles that the images are    contained in are overlapping.  This is the default.  - The "circle" method will determine if circles centered at the sprites'    positions are overlapping.  To use circle collision, you need to    specify a `.radius` attribute for the sprites or the circle will be    the smallest circle that encloses the entire image.  - The "mask" method will determine if the non-transparent parts of the    images are overlapping.  - You can pass in a custom function that takes two sprites as arguments    and returns a Boolean value indicating if they are touching.

### `.is_touching_point(x, y=None, method='rect')` {#is_touching_point}

> Returns whether or not the sprite is touching a given point.
> 
> The `method` argument can be used to specify which type of collision detection to use:  - The "rect" method will determine if the point is inside of the rectangle    that the image is contained in.  This is the default.  - The "circle" method will determine if the point is inside of a circle    centered at the sprite's position.  To use circle collision, you need    to specify a `.radius` attribute for the sprite or the circle will be the    smallest circle that encloses the entire image.  - The "mask" method will determine if the point is touching a    non-transparent part of the image.  - You can pass in a custom function that takes two sprites as arguments    and returns a Boolean value indicating if they are touching.

### `.move_backward(distance)` {#move_backward}

> Move the sprite by the given `distance` in the opposite of the direction it is currently pointing.

### `.move_forward(distance)` {#move_forward}

> Move the sprite by the given `distance` in the direction it is currently pointing.

### `.on_click(func, button='left', method='rect', bleeds=False)` {#on_click}

> Add a function that will be called when the mouse is clicked on this sprite.
> 
> You can provide the following arguments for the function `func`:  - `x` - will provide x-coordinate of the mouse  - `y` - will provide y-coordinate of the mouse  - `pos` - will provide a tuple of the coordinates (x and y) of the mouse  - `button` - will provide the name of the mouse button used  - `sprite` - will provide the sprite object involved
> 
> You can specify which mouse button needs to be used for the click using the `button` parameter.  It's value needs to be one of "left", "center", "right", "scrollup" or "scrolldown".  The left button is the default.
> 
> The `method` can be used to specify which type of collision detection to use to see if the sprite was clicked on.  See `.is_touching_point()` for more details.
> 
> If multiple sprites are stacked, then the event will be triggered for the highest sprite with a click handler.  If `bleeds` is set to `True`, then if this sprite is clicked, the click event will bleed to sprites underneath it.

### `.on_drag(func, button='left')` {#on_drag}

> Add a function that will be called when the mouse dragged while clicking on this sprite.
> 
> You can provide the following arguments for the function `func`:  - `x` - will provide x-coordinate of the mouse  - `y` - will provide y-coordinate of the mouse  - `pos` - will provide a tuple of the coordinates (x and y) of the mouse  - `button` - will provide the name of the mouse button used  - `sprite` - will provide the sprite object involved
> 
> You can specify which mouse button needs to be used for the click using the `button` parameter.  It's value needs to be one of "left", "center", "right", "scrollup" or "scrolldown".  The left button is the default.

### `.on_release(func, button='left')` {#on_release}

> Add a function that will be called when the mouse is released after clicking on this sprite.
> 
> You can provide the following arguments for the function `func`:  - `x` - will provide x-coordinate of the mouse  - `y` - will provide y-coordinate of the mouse  - `pos` - will provide a tuple of the coordinates (x and y) of the mouse  - `button` - will provide the name of the mouse button used  - `sprite` - will provide the sprite object involved
> 
> You can specify which mouse button needs to be used for the click using the `button` parameter.  It's value needs to be one of "left", "center", "right", "scrollup" or "scrolldown".  The left button is the default.

### `.on_update(func)` {#on_update}

> Add a custom update function that will be called on every iteration of the event loop.
> 
> You can provide the following arguments for the function `func`:  - `sprite` - will provide the sprite object being updated

### `.show()` {#show}

> Add the sprite to the active screen.

### `.turn_left(angle)` {#turn_left}

> Turn the sprite left (counterclockwise) by the given `angle`.

### `.turn_right(angle)` {#turn_right}

> Turn the sprite right (clockwise) by the given `angle`.

### `.turn_toward(x, y=None)` {#turn_toward}

> Turn the sprite towards the given coordinates.

### `.update(screen=None)` {#update}

> Update the sprite in preparation to draw the next frame.
> 
> This method should generally not be called explicitly, but will be called by the event loop if the sprite is on the active screen.

### `.anchor` {#anchor}

> The point on the image that will be placed on the sprite's position and used as the center of gravity for scaling and rotation.
> 
> The anchor point is a 2-tuple that can be:  - a point relative to the center of the image (e.g. `(50, -25)`)  - position descriptions including "center", "left", "right", "bottom"    and "top" (e.g. `("left", "center")`)  - a combination of the two (e.g. `("center", -25)`)
> 
> Note that the anchor is relative to the original image and scaling and rotation are done after the image is placed at the anchor point.

### `.bottom_edge` {#bottom_edge}

> The y-coordinate of the bottom edge of the sprite's image.

### `.bottom_edge_midpoint` {#bottom_edge_midpoint}

> The coordinates of the midpoint of the bottom edge of the sprite's image.

### `.bottom_left_corner` {#bottom_left_corner}

> The coordinates of the bottom left corner of the sprite's image.

### `.bottom_right_corner` {#bottom_right_corner}

> The coordinates of the bottom right corner of the sprite's image.

### `.center` {#center}

> The coordinates of the center of the sprite's image.

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

### `.disabled` {#disabled}

> Whether or not the sprite is disabled for click events.

### `.fill_color` {#fill_color}

> The current fill color.
> 
> The color can be one of the following values:  - A valid color string.  See https://replit.com/@cjdevet/PygameColors    to explore the available color strings.  - A set of three numbers between 0 and 255 that represent the    amount of red, green, blue to use in the color.  A fourth transparency    value can be added.  - An HTML color code in the form "#rrggbb" where each character    r, g, b and a are replaced with a hexidecimal digit.  For translucent    colors, add another pair of hex digits ("##rrggbbaa").  - An integer that, when converted to hexidecimal, gives an HTML color    code in the form 0xrrggbbaa.  - A pygame Color object.

### `.flipped` {#flipped}

> Whether or not the original picture is flipped.
> 
> This property is a 2-tuple of booleans that contains whether the image is flipped horizontally and vertically, respectively.

### `.flipped_horizontally` {#flipped_horizontally}

> Whether or not the original picture is flipped horizontally.

### `.flipped_vertically` {#flipped_vertically}

> Whether or not the original picture is flipped vertically.

### `.height` {#height}

> The height of the sprite's image.

### `.left_edge` {#left_edge}

> The x-coordinate of the left edge of the sprite's image.

### `.left_edge_midpoint` {#left_edge_midpoint}

> The coordinates of the midpoint of the left edge of the sprite's image.

### `.line_color` {#line_color}

> The current line color.
> 
> The color can be one of the following values:  - A valid color string.  See https://replit.com/@cjdevet/PygameColors    to explore the available color strings.  - A set of three numbers between 0 and 255 that represent the    amount of red, green, blue to use in the color.  A fourth transparency    value can be added.  - An HTML color code in the form "#rrggbb" where each character    r, g, b and a are replaced with a hexidecimal digit.  For translucent    colors, add another pair of hex digits ("##rrggbbaa").  - An integer that, when converted to hexidecimal, gives an HTML color    code in the form 0xrrggbbaa.  - A pygame Color object.

### `.opacity` {#opacity}

> The opacity of the Sprite's image.
> 
> The opacity is on a scale from 0 to 1.  An opacity of 0 means the picture is fully transparent.  An opacity of 1 means the picture is fully opaque.

### `.picture` {#picture}

> The sprite's current picture.
> 
> The picture can be:  - The name of an image file.  - A list of points that create a polygon.  - A pygame Surface image.  - A predefined polygon (e.g. "circle", "square", "turtle")  - `None`, in which case the sprite will be a 1x1 transparent pixel.

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

### `.size` {#size}

> The dimensions (width and height) of the sprite's image

### `.smooth` {#smooth}

> Whether or not the image is smoothed when scaled or rotated.
> 
> By default, a quick and simple scale and rotation is applied.  This can cause images to be pixelated (when enlarged), loose detail (when shrunk), or be distorted (when rotating).  If you set `smooth` to be `True`, then each new pixel will be sampled and an average color will be used.  This makes to scaled and rotated images be more smooth, but takes longer.  You may want to avoid smooth scaling if you will be scaling or rotating the image very frequently.

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

