---
layout: default
title: Screen
parent: pygameplus
---
# Screen

A Screen represents a single game screen visible in the window.

At any one time there can be only one "active" screen that is visible. If a screen is active and another is opened, then the active screen is  replaced in the window.

Screen objects store the following information about a screen:  - Its dimensions and title  - The background color and/or image  - Any images that have been drawn on the screen

Methods are provided to do the following:  - Open a screen and make it active  - Change the dimensions, title or background  - Clear any images that have been drawn on the screen  - Add behaviour when the mouse clicks on the screen or when keyboard    keys are used when the screen is active

---

## Attribute Summary

### Methods

| <a href="#add">`add(*sprites, layer=0)`</a> | Add the sprites to this screen. |
| <a href="#cancel_timer">`cancel_timer(event_id)`</a> | Stop the timer with the given event ID. |
| <a href="#clear">`clear()`</a> | Clears the screen of all contents, including background images, drawings and sprites. |
| <a href="#clear_canvas">`clear_canvas(remove_sprites=False)`</a> | Clear everything that was drawn on the screen. |
| <a href="#clear_circle">`clear_circle(center, radius, remove_sprites=False)`</a> | Clear a circular part of the screen. |
| <a href="#clear_rect">`clear_rect(corner1, corner2, remove_sprites=False)`</a> | Clear a rectangular part of the screen. |
| <a href="#configure_grid">`configure_grid(**kwargs)`</a> | Configure the grid that can be drawn on the screen to aid in finding positions. |
| <a href="#draw">`draw(surface=None)`</a> | Draw the contents of the screen. |
| <a href="#from_pygame_coordinates">`from_pygame_coordinates(pygame_x, pygame_y=None)`</a> | Convert a point in the pygame coordinate space to the same point in  this screen's coordinate space. |
| <a href="#on_click">`on_click(func, button='left')`</a> | Add a function that will be called when the mouse clicks anywhere on this screen while it is active. |
| <a href="#on_key_hold">`on_key_hold(func, key=None)`</a> | Add a function that will be called when a keyboard key is held down while this screen is active. |
| <a href="#on_key_press">`on_key_press(func, key=None)`</a> | Add a function that will be called when a keyboard key is pressed while this screen is active. |
| <a href="#on_key_release">`on_key_release(func, key=None)`</a> | Add a function that will be called when a keyboard key is released while this screen is active. |
| <a href="#on_mouse_move">`on_mouse_move(func)`</a> | Add a function that will be called when the mouse is moved anywhere on this screen while it is active. |
| <a href="#on_release">`on_release(func, button='left')`</a> | Add a function that will be called when the mouse releases a button anywhere on this screen while it is active. |
| <a href="#on_timer">`on_timer(func, delay, repeat=False)`</a> | Call a function after a given amount of time (in milliseconds). |
| <a href="#open">`open()`</a> | Make this screen the active, visible screen in the window. |
| <a href="#redraw">`redraw()`</a> | Update and draw the screen in the open window. |
| <a href="#to_pygame_coordinates">`to_pygame_coordinates(x, y=None)`</a> | Convert a point in this screen's coordinate space to the same point  in the pygame coordinate space. |
| <a href="#update">`update(*args, **kwargs)`</a> | Calls the update() method on all Sprites on the screen. |

**Inherited from `pygame.sprite.LayeredUpdates`:**

- `add_internal(sprite, layer=None)`
- `change_layer(sprite, new_layer)`
- `get_bottom_layer()`
- `get_layer_of_sprite(sprite)`
- `get_sprite(idx)`
- `get_sprites_at(pos)`
- `get_sprites_from_layer(layer)`
- `get_top_layer()`
- `get_top_sprite()`
- `layers()`
- `move_to_back(sprite)`
- `move_to_front(sprite)`
- `remove_internal(sprite)`
- `remove_sprites_of_layer(layer_nr)`
- `sprites()`
- `switch_layer(layer1_nr, layer2_nr)`

**Inherited from `pygame.sprite.AbstractGroup`:**

- `copy()`
- `empty()`
- `has(*sprites)`
- `has_internal(sprite)`
- `remove(*sprites)`

### Properties

| <a href="#background_color">`background_color`</a> | The background color of the screen. |
| <a href="#background_image">`background_image`</a> | The background image of the screen. |
| <a href="#canvas">`canvas`</a> | The image of any drawings that were drawn on the screen. |
| <a href="#height">`height`</a> | The height of the screen. |
| <a href="#is_open">`is_open`</a> | Return whether or not this screen is the active screen. |
| <a href="#show_grid">`show_grid`</a> | Whether or not the screen's grid is shown. |
| <a href="#size">`size`</a> | The size of the screen as a tuple with width and height. |
| <a href="#title">`title`</a> | The title of the screen that appears at its top. |
| <a href="#width">`width`</a> | The width of the screen. |

---

## Attribute Details

### `add(*sprites, layer=0)` {#add}

> Add the sprites to this screen.
> 
> The arguments can be individual sprite objects or a list of sprites.

### `background_color` {#background_color}

> The background color of the screen.
> 
> The color can be one of the following values:  - A valid color string.  See https://replit.com/@cjdevet/PygameColors    to explore the available color strings.  - A set of three numbers between 0 and 255 that represent the    amount of red, green, blue to use in the color.  A fourth transparency    value can be added.  - An HTML color code in the form "#rrggbb" where each character     r, g, b and a are replaced with a hexidecimal digit.  For translucent    colors, add another pair of hex digits ("##rrggbbaa").  - An integer that, when converted to hexidecimal, gives an HTML color    code in the form 0xrrggbbaa.  - A pygame Color object.
> 
> If this property is changed, it won't be reflected on the screen until it is redrawn.

### `background_image` {#background_image}

> The background image of the screen.
> 
> This image will be placed in the center of the screen.
> 
> The image can be:  - The file name of an image file.  - A Python file-like object created using open().  - `None` to remove any background image.
> 
> If this property is changed, it won't be reflected on the screen until it is redrawn.

### `cancel_timer(event_id)` {#cancel_timer}

> Stop the timer with the given event ID.
> 
> `event_id` must be an event ID that was returned from the `on_timer()` method for this EventLoop.

### `canvas` {#canvas}

> The image of any drawings that were drawn on the screen.

### `clear()` {#clear}

> Clears the screen of all contents, including background images, drawings and sprites.

### `clear_canvas(remove_sprites=False)` {#clear_canvas}

> Clear everything that was drawn on the screen.

### `clear_circle(center, radius, remove_sprites=False)` {#clear_circle}

> Clear a circular part of the screen.

### `clear_rect(corner1, corner2, remove_sprites=False)` {#clear_rect}

> Clear a rectangular part of the screen.

### `configure_grid(**kwargs)` {#configure_grid}

> Configure the grid that can be drawn on the screen to aid in finding positions.
> 
> Provide the following keyword arguments to change a property:  - x_dist (100)  - y_dist (100)  - color ("black")  - opacity (0.5)  - thickness (3)  - x_minor_dist (20)  - y_minor_dist (20)  - minor_color (same as color)  - minor_opacity (50% of opacity)  - minor_thickness (50% of thickness)

### `draw(surface=None)` {#draw}

> Draw the contents of the screen.
> 
> This method should generally not be called explicitly, but will be called by the event loop if the screen is active.
> 
> By default, this will draw the contents on the pygame Surface associated with this screen.  However, you can draw the screen's contents to another surface using this method by explicitely supplying a `surface` argument.

### `from_pygame_coordinates(pygame_x, pygame_y=None)` {#from_pygame_coordinates}

> Convert a point in the pygame coordinate space to the same point in  this screen's coordinate space.

### `height` {#height}

> The height of the screen.
> 
> Changing this property will immediately resize the screen.

### `is_open` {#is_open}

> Return whether or not this screen is the active screen.

### `on_click(func, button='left')` {#on_click}

> Add a function that will be called when the mouse clicks anywhere on this screen while it is active.
> 
> You can provide the following arguments for the function `func`:  - `x` - will provide x-coordinate of the click  - `y` - will provide y-coordinate of the click  - `pos` - will provide a tuple of the coordinates (x and y) of the click  - `button` - will provide the name of the mouse button used to click

### `on_key_hold(func, key=None)` {#on_key_hold}

> Add a function that will be called when a keyboard key is held down while this screen is active.
> 
> The given function will be called once for every frame of the event loop that passes while the key is held down.
> 
> You can provide the following arguments for the function `func`:  - `key` - will provide the name of the key
> 
> The `key` is a string specifying which key this function applies to.  If no `key` is given, then this function will apply any key that does not  have a handler.

### `on_key_press(func, key=None)` {#on_key_press}

> Add a function that will be called when a keyboard key is pressed while this screen is active.
> 
> You can provide the following arguments for the function `func`:  - `key` - will provide the name of the key
> 
> The `key` is a string specifying which key this function applies to.  If no `key` is given, then this function will apply any key that does not  have a handler.

### `on_key_release(func, key=None)` {#on_key_release}

> Add a function that will be called when a keyboard key is released while this screen is active.
> 
> You can provide the following arguments for the function `func`:  - `key` - will provide the name of the key
> 
> The `key` is a string specifying which key this function applies to.  If no `key` is given, then this function will apply any key that does not  have a handler.

### `on_mouse_move(func)` {#on_mouse_move}

> Add a function that will be called when the mouse is moved anywhere on this screen while it is active.
> 
> You can provide the following arguments for the function `func`:  - `x` - will provide x-coordinate of the click  - `y` - will provide y-coordinate of the click  - `pos` - will provide a tuple of the coordinates (x and y) of the click

### `on_release(func, button='left')` {#on_release}

> Add a function that will be called when the mouse releases a button anywhere on this screen while it is active.
> 
> You can provide the following arguments for the function `func`:  - `x` - will provide x-coordinate of the click  - `y` - will provide y-coordinate of the click  - `pos` - will provide a tuple of the coordinates (x and y) of the click  - `button` - will provide the name of the mouse button used to click

### `on_timer(func, delay, repeat=False)` {#on_timer}

> Call a function after a given amount of time (in milliseconds).
> 
> The function `func` will be called after `delay` milliseconds.  `func` must be a function that takes no arguments.  The `delay` must be a  positive number.
> 
> If `repeat` is `True`, then the timer will run repeatedly.  That is, the timer will restart every time that it expires.
> 
> An event ID will be returned that can be used with the `cancel_timer()` method to stop the timer.
> 
> If the screen is closed this timer will be closed.  To prevent this behaviour, create a global timer on the event loop.

### `open()` {#open}

> Make this screen the active, visible screen in the window.

### `redraw()` {#redraw}

> Update and draw the screen in the open window.
> 
> This method calls update() and draw(), then flips the changes to the  visible screen.

### `show_grid` {#show_grid}

> Whether or not the screen's grid is shown.

### `size` {#size}

> The size of the screen as a tuple with width and height.
> 
> Changing this property will immediately resize the screen.

### `title` {#title}

> The title of the screen that appears at its top.

### `to_pygame_coordinates(x, y=None)` {#to_pygame_coordinates}

> Convert a point in this screen's coordinate space to the same point  in the pygame coordinate space.

### `update(*args, **kwargs)` {#update}

> Calls the update() method on all Sprites on the screen.
> 
> This method should generally not be called explicitly, but will be called by the event loop if the screen is active.
> 
> This will pass this screen to the sprites' update() methods as the `screen` keyword argument.

### `width` {#width}

> The width of the screen.
> 
> Changing this property will immediately resize the screen.

