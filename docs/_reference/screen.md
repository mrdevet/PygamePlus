# Screen

A Screen represents a single game screen visible in the window.

At any one time there can be only one "active" screen that is visible.  If a screen is active and another is opened, then the active screen is replaced in the window.

Screen objects store the following information about a screen:
 - Its dimensions and title
 - The background color and/or image
 - Any images that have been drawn on the screen

Methods are provided to do the following:
 - Open a screen and make it active
 - Change the dimensions, title or background
 - Clear any images that have been drawn on the screen
 - Add behaviour when the mouse clicks on the screen or when keyboard keys are used when the screen is active

## Creation

To create a screen, you must provide a width and height.  You may also provide a title.

```python
# Create a screen that is 540px wide and 360px high
my_screen = Screen(540, 360, title='My Game')
```

Note that creating a screen does not open it.  You must use the `.open()` method to make it appear on the screen.

## Screen Size and State

Basic properties of the screen, including size, color and open state can be accessed or changed using these properties and methods:

| Property/Method | Description |
| --- | --- |
| `.is_open` | Whether or not this screen is the active screen.  This property is readonly.  Use the `.open()` method to open a non-active screen. |
| `.open()` | Open this screen.  This action will close any other active screen. |
| `.title` | The title that appears in the screen's header. |
| `.background_color` | The color of the screen's background.  This can be a color name, a 3-tuple of RGB colors, an HTML color code (`#rrggbb`), an integer whose hex value is an HTML color code, or a pygame `Color` object.  (default: `'white'`) |
| `.background_image` | The image file used as the screen's background.  This will appear on top of the background color.  To remove the background image, set this to `None`.  (default: `None`) |
| `.height` | The height of the screen, in pixels. |
| `.width` | The width of the screen, in pixels. |
| `.size` | The size of the screen, in pixels, as a (width, height) tuple. |

## Sprites on the Screen

The following methods can be used to manage the sprites that appear on the screen:

| Property/Method | Description |
| --- | --- |
| `.add(*sprites, layer=0)` | Add the sprites to this screen on the given layer.  The arguments can be individual sprite objects or a list of sprites. |
| `.remove(*sprites)` | Remove the sprite(s) from the screen. |
| `.has(*sprites)` | Returns whether or not all of the sprites are on the screen.  Alternatively, for one sprite, you can use the `in` operator. |
| `.sprites()` | Returns a list of sprites on the screen, ordered from back to front. |
| `.empty()` | Remove all sprites from the screen. |
| `.clear()` | Clears the screen of all contents, including backgrounds, canvas drawings and sprites. |

The `Screen` class is a subclass of pygame's group class `pygame.sprite.LayeredUpdates`. 
 More advanced sprite management can be done with that [class' methods](https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.LayeredUpdates).

## Coordinate System

PygamePlus uses a coordinate system that will look familiar to math students.  It has the origin at the center of the screen, positive x-coordinates go to the right and positive y-coordinates go up.  **This is different from pygame's coordinate system.**

The `Screen` class has methods to convert between these coordinate systems.  It also has a built-in grid that can be displayed to help developers locate positions on the screen.

| Property/Method | Description |
| --- | --- |
| `.show_grid` | Whether or not the screen's grid is being shown. (default: `False`) |
| `.configure_grid(**props)` | Configure the screen's grid.  It's properties include `x_dist`, `y_dist`, `color`, `opacity`.  For more, see this function's `help()` function output. |
| `.from_pygame_coordinates(x, y)` | Convert pygame coordinates into PygamePlus coordinates. |
| `.to_pygame_coordinates(x, y)` | Convert PygamePlus coordinates into pygame coordinates. |

## Screen Canvas

A screen can be drawn on using the `Painter` and `Turtle` sprite subclasses.  The following properties and methods can be used to manage this canvas.

| Property/Method | Description |
| --- | --- |
| `.canvas` | The `pygame.Surface` object representing the screen's canvas.  This property is readonly, but can be used with pygame's methods to alter the canvas. |
| `.clear_canvas(remove_sprites=False)` | Clears all contents of the screen's canvas.  Optionally, you can clear sprites from the screen. |
| `.clear_circle(center, radius, remove_sprites=False)` | Clears a circular section of the canvas with the given center position and radius. Optionally, you can clear sprites located in this circle.  |
| `.clear_rect(corner1, corner2, remove_sprites=False)` | Clears a rectangular section of the canvas with the given opposite corner positions. Optionally, you can clear sprites located in this rectangle. |

## Event Handlers

Event handler functions may be bound to the screen to be executed when mouse and keyboard events occur on the active screen.  Timers can also be created to execute a function when they expire.

The methods below are used to bind event handler functions to screen events.  If the function provided has certain named arguments, they will be used to pass event information (e.g. mouse location, key) to the handler.

| Property/Method | Description |
| --- | --- |
| `.on_click(func, button='left')` | Bind a function to mouse click down events.  Optionally, you can specify which mouse button to bind to (`'left'`, `'right'`, `'middle'`, `'scrollup'`, `'scrolldown'`).  The handler function can have these arguments: `x`, `y`, `pos`, `button`. |
| `.on_release(func, button='left')` | Bind a function to mouse release events.  Optionally, you can specify which mouse button to bind to (`'left'`, `'right'`, `'middle'`, `'scrollup'`, `'scrolldown'`).  The handler function can have these arguments: `x`, `y`, `pos`, `button`. |
| `.on_mouse_move(func)` | Bind a function to mouse movement events.  The handler function can have these arguments: `x`, `y`, `pos`. |
| `.on_key_hold(func, key=None)` | Bind a function that will be repeatedly called as long as a key is held down.  If no key is specified, this applies to all keys without their own handler.  The handler function can have these arguments: `key`. |
| `.on_key_press(func, key=None)` | Bind a function that will be called once when a key is pressed down.  If no key is specified, this applies to all keys without their own handler.  The handler function can have these arguments: `key`. |
| `.on_key_release(func, key=None)` | Bind a function that will be called once when a key is released.  If no key is specified, this applies to all keys without their own handler.  The handler function can have these arguments: `key`. |
| `.on_timer(func, delay, repeat=False)` | Call a function after a given time delay (in milliseconds).  Optionally, you can set this timer to repeat after it has expired.  The function returns an event ID that can be used to cancel the timer. |
| `.cancel_timer(event_id)` | Cancel the timer with the given event ID. |

## Updating and Drawing the Screen

The following methods are provided to update sprites and redraw the screen.  **These functions should not be used explicitly, but will be called by the game loop.**

| Property/Method | Description |
| --- | --- |
| `.update(*args, **kwargs)` | Calls the update function on all sprites on the screen.  All arguments will be passed to the sprites' update methods. |
| `.draw(surface=None)` | Draw the contents of the screen.  This can be used to take a snapshot of the screen. |
| `redraw()` | Update and draw the screen.  A convenience method that calls `.update()` and `.draw()`. |