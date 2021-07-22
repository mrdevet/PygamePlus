# Copyright 2021 Casey Devet
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.


############################################################
#                    MODULE DESCRIPTION
############################################################

"""
This module implements turtle graphics using the pygame
library.  It contains most of the methods in the original
turtle library.  Some features are enhanced, new features
added and some features removed.

The documentation for the original turtle module can be
found here: https://docs.python.org/3/library/turtle.html

TODO: Add a list of new features.
"""

############################################################
#                     GLOBAL VARIABLES
############################################################

import math
import pygame
import collections
from pygame.locals import *

# Initialize the pygame modules
pygame.init()

# The background information
_bgcolor = "white"
_bgpic = None
_bgpic_name = "nopic"
_bgpic_rect = None

# Stores the turtles that were clicked on with the mouse buttons
_clicked_sprite = {}

# Mapping of the collision method strings to their pygame
# functions for use in Turtle.is_collision()
_collision_functions = {
    "rect": pygame.sprite.collide_rect,
    "circle": pygame.sprite.collide_circle,
    "mask": pygame.sprite.collide_mask
}

# Stores the color mode being used.  This is either 1.0 or 255
_colormode = 1.0

# A list of handlers for custom events
_custom_events = []

# Stores the delay between frames and the frame rate.  These
# Should have the relationship _delay * _frame_rate = 1000
_delay = 20
_frame_rate = 50

# Store the fonts that are used in the game
_fonts = {}

# Store the angle that represents a full circle
_fullcircle = 360

# Store functions to be called on keyboard events
_keyhold_funcs = {}
_keypress_funcs = {}
_keyrelease_funcs = {}

# Stores the last ID used for a turtle stamp
_last_stamp_id = 0

# Stores whether the main loop is currently running
_running = False

# Holds the pygame screen object
_screen = None

# Store functions to be called on screenclick events
_screenclick_handlers = {}

# A group of all the turtles
_sprite_group = pygame.sprite.OrderedUpdates()

# Mapping of shape names to their images
# TODO: Make polygon shapes (turtle, square, circle, etc.)
_shapes = {
    "turtle": ((16, 0), (14, -2), (10, -1), (7, -4), (9, -7), (8, -9), (5, -6), 
               (1, -7), (-3, -5), (-6, -8), (-8, -6), (-5, -4), (-7, 0), (-5, 4), 
               (-8, 6), (-6, 8), (-3, 5), (1, 7), (5, 6), (8, 9), (9, 7), (7, 4), 
               (10, 1), (14, 2)),
    "square": ((10, -10), (10, 10), (-10, 10), (-10, -10)),
    "circle": ((10, 0), (9.51, 3.09), (8.09, 5.88), (5.88, 8.09), 
               (3.09, 9.51), (0, 10), (-3.09, 9.51), (-5.88, 8.09), 
               (-8.09, 5.88), (-9.51, 3.09), (-10, 0), (-9.51, -3.09), 
               (-8.09, -5.88), (-5.88, -8.09), (-3.09, -9.51), (-0.0, -10.0), 
               (3.09, -9.51), (5.88, -8.09), (8.09, -5.88), (9.51, -3.09))
}

# Flag that tells the mainloop that an update is necessary
_update_scheduled = False


############################################################
#                     HELPER FUNCTIONS
############################################################

def _draw_line (surface, color, start, end, width=1):
    '''
    Draws a line on a surface.

    This function replaces the pygame function for drawing a line
    on a surface.  This uses dots so that the lines are drawn
    with a consistent width no matter the angle and so the ends
    are capped.
    '''

    # If width is 1, use the pygame function
    if width == 1:
        pygame.draw.line(surface, color, start, end)

    # Otherwise use dots instead
    else:
        # Find geometric properties of the line
        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]
        radians = math.atan2(delta_y, delta_x) % math.tau
        distance = math.hypot(delta_x, delta_y)

        # Draw dots every 0.1 pixels along the line between
        # the points
        x, y = start
        pygame.draw.circle(surface, color, start, width / 2)
        for _ in range(round(distance * 10)):
            x += 0.1 * math.cos(radians)
            y += 0.1 * math.sin(radians)
            pygame.draw.circle(surface, color, (x, y), width / 2)


def _draw_lines (surface, color, points, width=1):
    '''
    Draws lines along a path of points.
    
    This function is a wrapper that repeatedly calls draw_line()
    '''

    # Loop through each pair of adjacent points and call _draw_line()
    for start, end in zip(points[:-1], points[1:]):
        _draw_line(surface, color, start, end, width)


def _make_color (*args):
    '''
    Convert color arguments to a pygame.Color object
    '''

    num_args = len(args)
    if num_args == 1 and isinstance(args[0], str):
        return pygame.Color(args[0])
    if num_args == 3 or num_args == 4:
        tup = args
    elif num_args == 1 and (isinstance(args[0], list) or isinstance(args[1])):
        tup = tuple(args[0])
    else:
        raise ValueError("Invalid color arguments!")
    if _colormode == 1:
        tup = tuple([int(x * 255) for x in tup])
    return pygame.Color(*tup)


def _pygame_location (turtle_x, turtle_y=None, width=None, height=None):
    '''
    Convert turtle coordinates to pygame coordinates.

    The turtle module uses a coordinate system with (0, 0)
    at the center of the screen and positive coordinates go
    up and right.
    
    The pygame module uses a coordinate system with (0, 0)
    at the top left corner and positive coordinates go down
    and right.
    '''

    if turtle_y is None:
        turtle_x, turtle_y = turtle_x
    if height is None:
        height = width
    if width is None:
        width, height = _screen.get_size()
    pygame_x = turtle_x + width / 2
    pygame_y = height / 2 - turtle_y
    return pygame_x, pygame_y


def _turtle_location (pygame_x, pygame_y=None, width=None, height=None):
    '''
    Convert pygame coordinates to turtle coordinates.

    The turtle module uses a coordinate system with (0, 0)
    at the center of the screen and positive coordinates go
    up and right.
    
    The pygame module uses a coordinate system with (0, 0)
    at the top left corner and positive coordinates go down
    and right.
    '''

    if pygame_y is None:
        pygame_x, pygame_y = pygame_x
    if height is None:
        height = width
    if width is None:
        width, height = _screen.get_size()
    turtle_x = pygame_x - width / 2
    turtle_y = height / 2 - pygame_y
    return turtle_x, turtle_y


def _update ():
    '''
    Update the screen.
    
    When the mainloop is running, it is called once per frame.  
    Otherwise, it is only called by the global update() function.
    '''

    # Add the background color and image
    _screen.fill(_bgcolor)
    if _bgpic is not None:
        _screen.blit(_bgpic, _bgpic_rect)

    # Call the update function for each turtle.  This puts
    # the turtle's rectangle in the correct position.
    _sprite_group.update()

    # For each turtle, add the drawings and stamps
    for sprite in _sprite_group:
        _screen.blit(sprite._canvas, (0, 0))
        for stamp in sprite._stamps.values():
            _screen.blit(*stamp)

    # Add each visible turtle to the screen
    for sprite in _sprite_group:
        if sprite._visible:
            _screen.blit(sprite.image, sprite.rect)

    # Put the new image to the screen
    pygame.display.update()

    # Drop the flag that says an update is needed
    _update_scheduled = False


############################################################
#                       TURTLE CLASS
############################################################

class Turtle (pygame.sprite.Sprite):
    '''
    A super-charged turtle.
    '''
    
    # TODO: make default shape
    def __init__ (self, shape=None):
        '''
        Create a Turtle object.

        Optionally, you can set the shape of the turtle on creation.
        The shape needs to be registered using the addshape() function.
        '''

        # Call the constructor for the parent Sprite class
        pygame.sprite.Sprite.__init__(self)

        # Create stamps dictionary and canvas
        self._stamps = collections.OrderedDict()
        self._canvas = pygame.Surface(_screen.get_size(),
                                      pygame.SRCALPHA)

        # Create dictionaries that hold mouse event handlers
        self._click_handlers = {}
        self._release_handlers = {}
        self._drag_handlers = {}

        # Create the shape
        if shape is None:
            self._original = pygame.Surface((1, 1))
        else:
            self.shape(shape)

        # Initialize all of the attributes
        self.reset()

        # Add the turtle to the group that holds all of the turtles
        _sprite_group.add(self)


    def _draw_poly_shape (self, new_surface=False):
        xscale = getattr(self, "_xscale", 1)
        yscale = getattr(self, "_yscale", 1)
        x_values = [x * xscale for x, y in self._poly]
        y_values = [y * yscale for x, y in self._poly]
        if new_surface or not hasattr(self, "_original"):
            x_min = min(x_values)
            x_max = max(x_values)
            y_min = min(y_values)
            y_max = max(y_values)

            width = x_max - x_min + 1
            height = y_max - y_min + 1
            self._original = pygame.Surface((width, height), pygame.SRCALPHA)
            
            self._pygame_poly = [(x - x_min, y_max - y) for x, y in
                                 zip(x_values, y_values)]

            self._xoffset = (x_min + x_max) / 2
            self._yoffset = (y_min + y_max) / 2

        fillcolor = getattr(self, "_fillcolor", "black")
        pencolor = getattr(self, "_pencolor", "black")
        pensize = getattr(self, "_pensize", 1)
        pygame.draw.polygon(self._original, fillcolor, self._pygame_poly)
        pygame.draw.polygon(self._original, pencolor, self._pygame_poly, pensize)


    def backward (self, distance):
        '''
        Move the turtle backwards.

        The turtle will move in the opposite direction of its heading
        by `distance` pixels.

        If the pen is down, this will draw a line alone the turtle's path.
        '''

        radians = self._heading / _fullcircle * math.tau
        self.goto(self._xcor - distance * math.cos(radians),
                  self._ycor - distance * math.sin(radians))

                
    def begin_fill (self):
        '''
        Start creating a filled shape.

        This function must be followed with a call to end_fill() which
        will draw the filled shape using all of the points visited
        from the call of this method.
        '''

        self._filling = True
        self._fillpoly = [(self._xcor, self._ycor, None, None, None)]


    def circle (self, radius, extent=None, steps=None):
        '''
        Draw a circle counterclockwise.

        The circle will have the given `radius`.  The `extent` is used to
        draw an arc around a portion of a circle.  If extent is negative,
        draw the circle clockwise.

        The circle will actually be an approximation.  The turtle will really
        draw a regular polygon with `steps` sides.
        '''

        start_pos = self._xcor, self._ycor

        # Sanitize extent argument
        if extent is None:
            extent = 360
        else:
            extent = int(extent)

        # Set up the number of steps and the turn angle needed between
        # steps.
        if steps is None:
            steps = abs(extent)
            turn_size = 1 if radius >= 0 else -1
        else:
            steps = abs(round(extent / 360 * steps))
            turn_size = abs(extent / steps)
            if radius < 0:
                turn_size = -turn_size
        step_size = abs(radius) * 2 * math.pi / 360

        # Repeatedly move forward and turn to approximate the circle
        for _ in range(steps):
            if extent > 0:
                self.forward(step_size)
                self.left(turn_size)
            else:
                self.right(turn_size)
                self.backward(step_size)

        # If we did a full circle, ensure that we end up exactly where 
        # we started.  If we don't do this, rounding could make us slightly
        # off target.
        if extent % 360 == 0:
            self._xcor, self._ycor = start_pos


    def clear (self):
        '''
        Clear all of the turtle's drawing, writing and stamps.
        '''

        self._canvas = pygame.Surface(_screen.get_size(),
                                      pygame.SRCALPHA)
        self._stamps.clear()


    def clearstamp (self, stampid):
        '''
        Remove the stamp with the given id.
        '''

        self._stamps.pop(stampid)


    def clearstamps (self, n=None):
        '''
        Remove all of the turtle's stamps.

        If an argument is given, the first `n` stamps will be removed.  If 
        `n` is negative that last `abs(n)` stamps will be removed.
        '''

        # If no argument, remove all stamps
        if n is None:
            self._stamps.clear()

        # If there is an argument, pop n items from the dictionary
        else:
            for _ in range(abs(min(n, len(self._stamps)))):
                # Pop from the start
                if n > 0:
                    self._stamps.popitem(last=False)

                # Pop from the end
                else:
                    self._stamps.popitem(last=True)
        

    def color (self, *args):
        '''
        Get or change the pen and fill color.

        If no arguments are given, this returns both the current pen color
        and fill color as a tuple.

        If one argument is given, both the pen and fill colors will be change 
        to it.  The argument can be:
        * A color string.
        * If colormode is 255, a tuple of three integers between 0 and 255
          representing the amount of red, blue and green.
        * If colormode is 1.0, a tuple of three floats between 0 and 1
          representing the amount of red, blue and green.

        If two arguments are given, the pen color will be set to the first and 
        the fill color will be set to the second.
        '''

        # If no arguments, return current colors
        if len(args) == 0:
            return self._pencolor, self._fillcolor

        # If two arguments, change pen color to first and fill color to
        # second
        if len(args) == 2:
            self.pencolor(args[0])
            self.fillcolor(args[1])

        # Otherwise, only one color given.  Change both colors.
        else:
            self.pencolor(*args)
            self.fillcolor(*args)


    def distance (self, x, y=None):
        '''
        Determine the distance between this turtle and another turtle or
        point.
        '''

        # If given a turtle, get its position
        if isinstance(x, Turtle):
            x, y = x.position()

        # If given a single argument, it must be a a tuple
        if y is None:
            x, y = x

        # Calculate the distance
        delta_x = x - self._xcor
        delta_y = y - self._ycor
        return math.hypot(delta_x, delta_y)


    def dot (self, size=None, color=None):
        '''
        Draw a dot.

        The dot will be centered at the current position and have diameter
        `size`.

        If the `color` is not specified, the pen color is used.
        '''

        # If no size is given, make the dot a bit bigger than the pen size
        if size is None:
            size = max(self._pensize + 4, 2 * self._pensize)

        # If no color is given use the pen color
        if color is None:
            color = self._pencolor_obj

        # Draw the dot
        point = _pygame_location(self._xcor, self._ycor)
        pygame.draw.circle(self._canvas, color, point, size / 2)


    def end_fill (self):
        '''
        Complete drawing a filled shape.

        This function must be preceded by a call to begin_fill().  When
        this method is called, a filled shape will be drawn using all of the
        points visited since begin_fill() was called.
        '''

        # Extract the points that make up the shape
        # Get all lines that were drawn since begin_fill().  These need
        # to be drawn again because the fill will cover part of them up.
        points = []
        redraw_lines = []
        last_point = None
        for x, y, pendown, pencolor, pensize in self._fillpoly:
            points.append(_pygame_location(x, y))
            if last_point is not None and pendown:
                redraw_lines.append((last_point, (x, y), 
                                     pencolor, pensize))
            last_point = (x, y)

        # Draw the fill
        pygame.draw.polygon(self._canvas, self._fillcolor, points)
                        
        # Redraw any lines around the fill
        for p1, p2, pencolor, pensize in redraw_lines:
            start = _pygame_location(p1)
            end = _pygame_location(p2)
            _draw_line(self._canvas, pencolor, start, end, pensize)
        
        # Reset the filling attributes
        self._filling = False
        self._fillpoly = None


    def fillcolor (self, *args):
        '''
        Get or change the color used for filled shapes.

        If no arguments are given, then this returns the current fill color.

        To change the color, the arguments can be:
        * One color string
        * If colormode is 255, three integers between 0 and 255
          representing the amount of red, blue and green.
        * If colormode is 1.0, three floats between 0 and 1
          representing the amount of red, blue and green.
        '''

        # If there are no arguments, return the current color
        if len(args) == 0:
            return self._fillcolor 

        # Store the color in the _fillcolor attribute
        if isinstance(args[0], list) or isinstance(args[0], tuple):
            self._fillcolor = tuple(args[0])
        elif isinstance(args[0], str):
            self._fillcolor = args[0]
        else:
            self._fillcolor = args

        # Create a color object using the arguments and the current
        # colormode
        self._fillcolor_obj = _make_color(*args)


    def filling (self):
        '''
        Get whether or not the turtle is currently drawing a filled shape.
        '''

        return self._filling


    def forward (self, distance):
        '''
        Move the turtle forwards.

        The turtle will move in the direction of its heading by `distance` 
        pixels.

        If the pen is down, this will draw a line alone the turtle's path.
        '''

        radians = self._heading / _fullcircle * math.tau
        self.goto(self._xcor + distance * math.cos(radians),
                  self._ycor + distance * math.sin(radians))


    def goto (self, x, y=None):
        '''
        Move the turtle to a specific location.

        If the pen is down, this will draw a line alone the turtle's path.
        '''

        # Sanitize the arguments
        if y is None:
            x, y = y.position() if isinstance(y, Turtle) else x

        # If the pen is down, draw a line along the turtle's path
        if self._pendown:
            old_point = _pygame_location(self._xcor, self._ycor)
            new_point = _pygame_location(x, y)
            _draw_line(self._canvas, self._pencolor, old_point,
                       new_point, self._pensize)

        # If the turtle is currently creating a filled shape, store
        # the point and the current pen information.
        if self._filling:
            self._fillpoly.append((x, y, self._pendown, 
                                   self._pencolor, self._pensize))

        # Change the coordinates of the turtle
        self._xcor = x
        self._ycor = y


    def heading (self):
        '''
        Get the turtle's current heading.
        '''

        return self._heading


    def hideturtle (self):
        '''
        Make the turtle invisible.
        '''

        self._visible = False


    def home (self):
        '''
        Move the turtle to the center of the screen.

        If the pen is down, this will cause drawing.
        '''

        self.goto(0, 0)


    def isdown (self):
        '''
        Get whether or not the pen is currently down and movement will cause
        drawing.
        '''

        return self._pendown


    def is_touching (self, other, method="rect"):
        '''
        Determine if the turtle is in collision with a point, turtle or list
        of turtles.

        You can provide a `method` that says what type of collision detection 
        to use:
        * "rect" - Rectangle collision
        * "circle" - Circle collision (to use this effectively, you need to 
          set a .radius attribute on each turtle)
        * "mask" - Collision only if non-transparent parts of the images are 
          touching.  This method is processor intensive and will cause lag if 
          used too many times per frame.
        '''

        # Get the collision detection function for the given method
        if isinstance(method, str):
            if method not in _collision_functions:
                raise ValueError(f"Invalid collision method: {method}")
            method = _collision_functions[method]

        # Update the turtle and, if dirty, get its mask
        self.update()
        if method == pygame.sprite.collide_mask and self._dirty:
            self.mask = pygame.mask.from_surface(self.image)

        # Collision detection if given a point
        if isinstance(other, tuple):
            return self.rect.collidepoint(_pygame_location(*other))

        # If given one turtle, put it into a list
        if isinstance(other, pygame.sprite.Sprite):
            other = [other]

        # If given a list, loop through it use the method from above
        if isinstance(other, list):
            for other_sprite in other:
                other_sprite.update()
                if method == pygame.sprite.collide_mask and other_sprite._dirty:
                    other_sprite.mask = pygame.mask.from_surface(other_sprite.image)
                if other_sprite.alive() and bool(method(self, other_sprite)):
                    return True
            return False
        
        # If given a pygame sprite group, use the pygame function for 
        # collision detection with a group
        elif isinstance(other, pygame.sprite.Group):
            other.update()
            hit_list = pygame.sprite.spritecollide(self, other, False, method)
            return len(hit_list) > 0

        # If given an invalid argument, just return False
        else:
            return False


    def isvisible (self):
        '''
        Get whether or not the turtle is currently visible on the screen.
        '''

        return self._visible


    def left (self, angle):
        '''
        Turn the turtle counterclockwise by the given `angle`.
        '''

        self.setheading(self._heading + angle)


    def onclick (self, func, button=1, add=None):
        '''
        Add an event handler for click events on the turtle.

        If given `None`, then all click event handlers are removed for that
        button.

        The `button` argument sets which mouse button on the mouse is used:
        * button=1 is the left mouse button
        * button=2 is the center mouse button
        * button=3 is the right mouse button
        * button=4 is scrolling the mouse scroller up
        * button=5 is scrolling the mouse scroller down

        If `add` is set to `False`, then all previously added handlers will
        removed.  Otherwise, this handler will replace the most previously
        added handler.
        '''

        # If None is given, remove all of the handlers
        if func is None:
            self._click_handlers.pop(button, None)

        # Otherwise, add the handler.  
        elif button in self._click_handlers:
            if add:
                self._click_handlers[button].append(func)
            else:
                # Replace the last handler added
                self._click_handlers[button][-1] = func
        else:
            self._click_handlers[button] = [func]


    def ondrag (self, func, button=1, add=None):
        '''
        Add an event handler for click and drag events on the turtle.

        If given `None`, then all event handlers are removed for that
        button.

        The `button` argument sets which mouse button on the mouse is used:
        * button=1 is the left mouse button
        * button=2 is the center mouse button
        * button=3 is the right mouse button
        * button=4 is scrolling the mouse scroller up
        * button=5 is scrolling the mouse scroller down

        If `add` is set to `False`, then all previously added handlers will
        removed.  Otherwise, this handler will replace the most previously
        added handler.
        '''

        # If None is given, remove all of the handlers
        if func is None:
            self._drag_handlers.pop(button, None)

        # Otherwise, add the handler. 
        elif button in self._drag_handlers:
            if add:
                self._drag_handlers[button].append(func)
            else:
                # Replace the last handler added
                self._drag_handlers[button][-1] = func
        else:
            self._drag_handlers[button] = [func]


    def onrelease (self, func, button=1, add=None):
        '''
        Add an event handler for mouse button release events on the turtle.

        If given `None`, then all event handlers are removed for that
        button.

        The `button` argument sets which mouse button on the mouse is used:
        * button=1 is the left mouse button
        * button=2 is the center mouse button
        * button=3 is the right mouse button
        * button=4 is scrolling the mouse scroller up
        * button=5 is scrolling the mouse scroller down

        If `add` is set to `False`, then all previously added handlers will
        removed.  Otherwise, this handler will replace the most previously
        added handler.
        '''

        # If None is given, remove all of the handlers
        if func is None:
            self._release_handlers.pop(button, None)

        # Otherwise, add the handler. 
        elif button in self._release_handlers:
            if add:
                self._release_handlers[button].append(func)
            else:
                # Replace the last handler added
                self._release_handlers[button][-1] = func
        else:
            self._release_handlers[button] = [func]


    def pencolor (self, *args):
        '''
        Get or change the color used for drawing lines and dots.

        If no arguments are given, then this returns the current pen color.

        To change the color, the arguments can be:
        * One color string
        * If colormode is 255, three integers between 0 and 255
          representing the amount of red, blue and green.
        * If colormode is 1.0, three floats between 0 and 1
          representing the amount of red, blue and green.
        '''

        # If there are no arguments, return the current color
        if len(args) == 0:
            return self._pencolor

        # Store the color in the _pencolor attribute
        if isinstance(args[0], list) or isinstance(args[0], tuple):
            self._pencolor = tuple(args[0])
        elif isinstance(args[0], str):
            self._pencolor = args[0]
        else:
            self._pencolor = args

        # Create a color object using the arguments and the current
        # colormode
        self._pencolor_obj = _make_color(*args)


    def pendown(self):
        '''
        Put the pen down so that movement will cause drawing.
        '''

        self._pendown = True


    def pensize (self, width=None):
        '''
        Get or change the size of the pen.

        If no argument is given, return the current pen size.

        Otherwise, change the pen size to the given `width`.
        '''

        # No argument, so return the current size
        if width is None:
            return self._pensize

        # Change the size
        self._pensize = width


    def penup (self):
        '''
        Pick the pen up so that movement will not cause drawing.
        '''

        self._pendown = False


    def position (self):
        '''
        Get the current x- and y-coordinates of the turtle.
        '''

        return self._xcor, self._ycor


    def reset (self):
        '''
        Delete the turtle’s drawings from the screen and re-center the turtle.
        
        This will also revert all of the turtle's settings to their defaults.
        All click event listeners will be removed.
        '''

        # Initialize/reset attributes for location, heading and visibility
        self._xcor = 0
        self._ycor = 0
        self._visible = True
        self._heading = 0

        # Initialize/reset attributes for drawing
        self._pendown = True
        self._pencolor = "black"
        self._pencolor_obj = pygame.Color("black")
        self._pensize = 1
        self._filling = False
        self._fillpoly = None
        self._fillcolor = "black"
        self._fillcolor_obj = pygame.Color("black")
        self._canvas.fill(0)
        self._stamps.clear()

        # Initialize/reset attributes for scaling and rotating
        self._yscale = 1
        self._xscale = 1
        self._xoffset = 0
        self._yoffset = 0
        self._outline = 1
        self._tilt = 0
        self._rotate_on_turn = False

        # Initialize/reset attributes that hold mouse event handlers
        self._click_handlers.clear()
        self._release_handlers.clear()
        self._drag_handlers.clear()

        # Create the shape
        self._scaled_image = self._original
        self.image = self._scaled_image
        self.rect = self._original.get_rect()
        self.rect.center = _pygame_location(0, 0)

        # Flag the is used to signify that the turtle has been changed
        # and the mask used for collision is not accurate
        self._dirty = True


    def right (self, angle):
        '''
        Turn the turtle clockwise by the given `angle`.
        '''

        self.setheading(self._heading - angle)


    def rotate_with_turn (self, do_rotate=None):
        '''
        Get or change whether or not the turtle's image rotates when the
        heading changes.

        If no argument is given, this will return the current setting.

        To change the setting, give either `True` or `False` as an arguments.
        '''

        # No argument, so return the current setting
        if do_rotate is None:
            return self._rotate_on_turn

        # Change the setting
        self._rotate_on_turn = bool(do_rotate)


    def setheading (self, to_angle):
        '''
        Set the direction that the turtle will move.

        The heading is an angle counterclockwise from the positive x-axis.
        '''

        # Make the angle positive and within one rotation
        self._heading = to_angle % _fullcircle

        # If the turtle rotates while turning, rotate the image
        if self._rotate_on_turn:
            angle = (self._heading + self._tilt) * 360 / _fullcircle
            self.image = pygame.transform.rotate(self._scaled_image, angle)
            self.rect = self.image.get_rect()
            self._dirty = True

        # Otherwise, set the tilt.  The tilt is the angle the image is 
        # currently rotated from its heading.
        else:
            self._tilt = (_fullcircle - self._heading) % _fullcircle


    def setx (self, x):
        '''
        Set the x-coordinate of the turtle's location.

        This does not change the y-coordinate.
        '''

        self.goto(x, self._ycor)


    def sety (self, y):
        '''
        Set the y-coordinate of the turtle's location.

        This does not change the x-coordinate.
        '''

        self.goto(self._xcor, y)


    def shape (self, name=None):
        '''
        Get or change the shape/image of the turtle.

        If no argument is given, return the current shape.  Otherwise, change
        the shape.

        The argument must be one of the built-in shapes or a shape registered
        with the addshape() function.

        Changing the shape removes any scaling.
        '''

        # If no argument is given, return the current shape
        if name is None:
            return self._shape

        # Raise an error if the shape is not a registered shape.
        if name not in _shapes:
            raise ValueError(f"There is no shape named {name}")

        # Retrieve the new shape
        new_shape = _shapes[name]

        # If the shape is a pygame Surface, then load it
        if isinstance(new_shape, pygame.Surface):
            self._original = new_shape

        # If the shape is a tuple, then we need to create a Surface with
        # these points
        elif isinstance(new_shape, tuple):
            self._poly = new_shape
            # raise NotImplementedError("Polygon shapes are not working yet!")
            self._draw_poly_shape(new_surface=True)
        
        # Set the rest of the attributes
        # TODO: I think rotation might not be being applied to the new
        # image.  Move any rotation to the update() function???
        self._scaled_image = self._original
        self.rect = self._original.get_rect()
        self.image = self._scaled_image.copy()
        self._dirty = True
        # self._xscale = 1 
        # self._yscale = 1
        self._shape = name


    def showturtle (self):
        '''
        Make the turtle visible on the screen.
        '''

        self._visible = True


    def stamp (self):
        '''
        Stamp a copy of the turtle's shape on the screen.

        An id will be returned that can be used to remove this one stamp.
        '''

        # Add a copy of the image to the stamps list and return a unique id
        global _last_stamp_id
        _last_stamp_id += 1
        rect = self.image.get_rect()
        rect.center = _pygame_location(self._xcor, self._ycor)
        self._stamps[_last_stamp_id] = (self.image.copy(), rect)
        return _last_stamp_id


    def tilt (self, angle):
        '''
        Tilt the image by the given angle.

        This does not change the turtle's heading.
        '''

        self.tiltangle(self._tilt + angle)


    def tiltangle (self, angle=None):
        '''
        Get or change how far the image is tilted from its heading.

        If no argument is given, get the current setting.  Otherwise, change
        the setting.

        This does not change the turtle's heading.
        '''

        # If no argument is given, return the current setting
        if angle is None:
            return self._tilt

        # Make the angle positive and within one rotation
        self._tilt = angle % _fullcircle

        # Rotate the image
        angle = (self._heading + self._tilt) * 360 / _fullcircle
        self.image = pygame.transform.rotate(self._scaled_image, angle)
        self.rect = self.image.get_rect()
        self._dirty = True


    def towards (self, x, y=None):
        '''
        Determine the direction from the turtle to another turtle or point.
        '''

        # If given a turtle, get its coordinates.
        if y is None:
            x, y = y.position() if isinstance(y, Turtle) else x

        # Calculate the heading
        delta_x = x - self._xcor
        delta_y = y - self._ycor
        radians = math.atan2(delta_y, delta_x) % math.tau
        return radians / math.tau * _fullcircle


    def turtlesize (self, stretch_wid=None, stretch_len=None, outline=None, smooth=True):
        '''
        Get or change the size of the turtle's shape.

        If no arguments are given, return the current width scale factor, 
        height scale factor and outline size.  Otherwise, change the settings
        and rescale the image.

        The turtle will be stretched (or compressed) by the factors given.
        The first argument is the factor that the width will be multiplied by
        and the second argument is the factor that the height will be 
        multiplied by.  If these numbers are the same, only one needs to be
        provided.

        The `outline` parameter changes the outline width of turtles that are
        polygons.

        By default, this method uses smooth scaling which can cause lagging
        for large pictures or if called very often.  A quicker but less 
        accurate scaling can be done by setting `smooth` to `False`.
        '''

        # TODO: Add outline size when polygon shapes are supported
        if outline is not None:
            raise Warning("Can't outline yet!")

        # If no arguments are given, return the current scaling factors
        # and outline width
        if stretch_wid is None:
            return (self._xscale, self._yscale, self._outline)

        # If only one factor is given, use it for the length and width
        if stretch_len is None:
            stretch_len = stretch_wid
        self._xscale = stretch_wid
        self._yscale = stretch_len
        
        # Set the outline attribute it was set
        if outline is not None:
            self._outline = outline

        # Get the new width and height and scale the image.
        new_width = round(self._xscale * self._original.get_width())
        new_height = round(self._yscale * self._original.get_height())
        if smooth:
            self._scaled_image = pygame.transform.smoothscale(self._original, (new_width, new_height))
        else:
            self._scaled_image = pygame.transform.scale(self._original, (new_width, new_height))

        # If necessary, rotate the image to match the current settings
        angle = (self._heading + self._tilt) * 360 / _fullcircle
        if angle == 0:
            self.image = self._scaled_image
        else:
            self.image = pygame.transform.rotate(self._scaled_image, angle)
        self.rect = self.image.get_rect()
        self._dirty = True


    def update (self):
        '''
        This function is necessary for sprites in pygame.  It should not be
        called.

        This method does not update the screen in any way.
        '''
        width, height = _screen.get_size()
        self.rect.centerx = self._xcor + width / 2 + self._xoffset
        self.rect.centery = height / 2 - self._ycor - self._yoffset


    def write (self, arg, move=False, align="bottom left", font="Arial", font_size=8, font_style="normal"):
        '''
        Write text to the screen at the turtle's current location.

        If `move` is set to `True` the turtle will move to the end of the text
        after writing.

        The `align` parameter sets where the turtle aligns with the text being
        written.  It is a string containing "left", "right", "center", "top",
        "bottom", "middle" or a combination separated by space (e.g. 
        "bottom center")

        The `font` parameter can be the name of a font on the system or a
        True Type Font file (.ttf) located in the directory.

        The `font_size` is the height of the text in pixels.
        
        The `font_style` argument can be "bold", "italic", "underline" or a 
        combination separated by space (e.g. "bold italic")
        '''

        # If font is a tuple/list, split it into separate variables.
        if isinstance(font, tuple) or isinstance(font, list):
            len_font = len(font)
            if len_font == 0:
                font = "Arial"
            if len_font == 1:
                font = font[0]
            if len_font == 2:
                font, font_size = font
            else:
                font, font_size, font_style = font[:3]

        # If font is a Font object, just use that
        if isinstance(font, pygame.font.Font):
            font_obj = font

        # If this font and size have been used before, check the _fonts cache
        if (font, font_size) in _fonts:
            font_obj = _fonts[font, font_size]

        # If the font ends in ".ttf", then load the font from the file
        elif font.endswith(".ttf"):
            font_obj = pygame.font.Font(font, font_size)
            _fonts[font, font_size] = font_obj

        # Otherwise, use a system font
        else:
            font_obj = pygame.font.SysFont(font, font_size)
            _fonts[font, font_size] = font_obj

        # Apply the styles
        if isinstance(font_style, str):
            font_style = font_style.split()
        font_style = [style.lower() for style in font_style]
        font_obj.set_bold("bold" in font_style)
        font_obj.set_italic("italic" in font_style)
        font_obj.set_underline("underline" in font_style)

        # Render an image of the text
        image = font_obj.render(str(arg), True, self._pencolor)
        rect = image.get_rect()

        # Set the positive of the text from the align parameter
        if isinstance(align, str):
            align = align.split()
        align = [location.lower() for location in align]
        x, y = _pygame_location(self._xcor, self._ycor)
        rect.left = x
        rect.bottom = y
        for location in align:
            if location == "left":
                rect.left = x
            elif location == "center":
                rect.centerx = x
            elif location == "right":
                rect.right = x
            elif location == "top":
                rect.top = y
            elif location == "middle":
                rect.centery = y
            elif location == "bottom":
                rect.bottom = y

        # Draw the text on the canvas
        self._canvas.blit(image, rect)

        # If move is True, move the turtle to the right side of the text
        if move:
            self._xcor = rect.right

        # Return a Font object that can be used for future writing
        return font_obj


    def xcor (self):
        '''
        Return the turtle's current x-coordinate.
        '''

        return self._xcor


    def ycor (self):
        '''
        Return the turtle's current y-coordinate.
        '''

        return self._ycor


############################################################
#                     GLOBAL FUNCTIONS
############################################################

def addshape (name, shape=None):
    '''
    Register an image or polygon as a turtle shape.

    Polygon shapes have not yet been implemented.
    '''

    # TODO: Implement polygon shapes
    if shape is not None:
        raise NotImplementedError("Can't create your own shapes yet!")
        
    _shapes[name] = pygame.image.load(name)


def bgcolor (*args):
    '''
    Get or change the background color of the screen.

    If no arguments are given, then this returns the current background color.

    To change the color, the arguments can be:
    * One color string
    * If colormode is 255, three integers between 0 and 255 representing the 
      amount of red, blue and green.
    * If colormode is 1.0, three floats between 0 and 1 representing the 
      amount of red, blue and green.
    '''

    global _bgcolor

    # If no arguments are given return the current color
    if len(args) == 0:
        return _bgcolor 

    # Set the color
    elif len(args) == 1:
        _bgcolor = args[0]
    else:
        _bgcolor = tuple(args)


def bgpic (picname=None):
    '''
    Get or change the background image on the screen.

    If no argument is given, this function returns the current background 
    picture.  Otherwise, the picture will be changed.

    The argument should be the name of a file in the directory.

    If `"nopic"` is given, then any background image will be removed.
    '''

    global _bgpic, _bgpic_name, _bgpic_rect

    # If no arguments are given, return the current image
    if picname is None:
        return _bgpic_name

    # If "nopic" is given, remove any background image
    if picname == "nopic":
        _bgpic = None
        _bgpic_name = "nopic"
        _bgpic_rect = None

    # Otherwise load the image and put it in the center of the
    # screen.
    else:
        _bgpic = pygame.image.load(picname)
        _bgpic_name = picname
        _bgpic_rect = _bgpic.get_rect()
        _bgpic_rect.centerx = _screen.get_width() / 2
        _bgpic_rect.centery = _screen.get_height() / 2


def bye ():
    '''
    End the mainloop.

    As long as there are no command after the turtle.mainloop() command, 
    this will end the program.
    '''

    global _running

    _running = False


def clearscreen ():
    '''
    Clear the screen of all drawings and turtles and remove all event 
    listeners.
    '''

    _sprite_group.empty()
    _screenclick_handlers.clear()
    bgpic("nopic")
    bgcolor("white")
    for event_index in range(len(_custom_events)):
        pygame.time.set_timer(USEREVENT + event_index, 0)
    _custom_events.clear()
    _keyhold_funcs.clear()
    _keypress_funcs.clear()
    _keyrelease_funcs.clear()


def colormode (cmode=None):
    '''
    Get or change the current colormode.

    If not argument is given, return the current colormode.  Otherwise, change
    it.

    The argument can be either 1.0 or 255.  This number is the maximum 
    possible value when creating colors using RGB numbers.
    '''

    global _colormode

    # If no argument given, return current setting
    if cmode is None:
        return _colormode

    # Change the setting only if 1 or 255 is given
    elif cmode == 1 or cmode == 255:
        _colormode = cmode


def degrees (fullcircle=360):
    '''
    Set the unit of measure for angles to degrees.

    If no argument is given, a full rotation is 360 degrees.  Otherwise,
    the argument will be the value used for a full rotation.
    '''

    global _fullcircle

    _fullcircle = fullcircle


def delay (delay=None):
    '''
    Get or change the delay used between frames of the mainloop.

    If no argument is given, then this function returns the current setting.
    Otherwise, the frame delay will be changed to the given value.

    NOTE: The frame rate (frames per second) will be `1000 / delay`.
    '''

    global _delay

    # If no argument is given, return the current setting
    if delay == None:
        return _delay

    # Change the settings
    _delay = delay
    _frame_rate = 1000 / delay


def getshapes ():
    '''
    Get a list of the available turtle shapes.
    '''

    return list(_shapes)


def listen (xdummy=None, ydummy=None):
    '''
    This function does nothing.

    It is included for compatibility with the original turtle module.
    '''
    pass


def mainloop (delay=None):
    '''
    Start the mainloop.

    The mainloop is loop that is continuously executed.  At every iteration
    of the loop, checks if any events have occurred and, if so, calls any
    event handlers that have been registered.  Events will not be processed
    until the mainloop has been started.

    Any initial page setup should be done before this function is called.  
    This function will be the last command in the program because when the 
    loop ends, the screen will be closed.  Any command afterward will not
    be executed.

    Every iteration of the loop will have a small delay between them.  This 
    affects how quite events are handled and how smooth animations appear.
    The `delay` argument will set this delay to be the given number of 
    milliseconds.  By default the frame delay is 20 milliseconds, creating
    a frame rate of 50 frames per second.

    The mainloop can be ended by calling `turtle.bye()` in one of your event
    handlers.
    '''

    global _running

    # Create a clock to make delays between frames
    clock = pygame.time.Clock()
    frame_rate = _frame_rate if delay is None else 1000 / delay

    # The mainloop continues as long as _running is True
    _running = True
    while _running:
        # Force the loop to wait if the entire frame delay has not passed 
        # since the start of the last iteration
        clock.tick(frame_rate)

        # Loop through the events that have occurred over the past frame
        for event in pygame.event.get():
            # If the close button is clicked, end the loop
            if event.type == QUIT:
                _running = False

            # If a custom event occurs, call its handler.  This is generally
            # used for timer events.
            elif event.type >= USEREVENT:
                try:
                    _custom_events[event.type - USEREVENT]()
                except IndexError:
                    pass

            # If a key was pressed, call any associated handlers
            elif event.type == KEYDOWN:
                if event.key in _keypress_funcs:
                    _keypress_funcs[event.key]()
                elif None in _keypress_funcs:
                    _keypress_funcs[None]()

            # If a key was released, call any associated handlers
            elif event.type == KEYUP:
                if event.key in _keyrelease_funcs:
                    _keyrelease_funcs[event.key]()
                elif None in _keyrelease_funcs:
                    _keyrelease_funcs[None]()

            # If a mouse button is clicked down, call any associated handlers
            elif event.type == MOUSEBUTTONDOWN:
                button = event.button
                for sprite in _sprite_group:
                    if sprite.rect.collidepoint(event.pos):
                        _clicked_sprite[button] = sprite
                        for func in sprite._click_handlers.get(button, []):
                            x, y = _turtle_location(*event.pos)
                            # TODO: Allow functions with less than two 
                            # parameters to be used.
                            func(x, y)
                        break
                for func in _screenclick_handlers.get(button, []):
                    x, y = _turtle_location(*event.pos)
                    func(x, y)

            # If a mouse button is released, call any associated handlers
            elif event.type == MOUSEBUTTONUP:
                button = event.button
                sprite = _clicked_sprite.pop(button, None)
                if sprite:
                    for func in sprite._release_handlers.get(button, []):
                        x, y = _turtle_location(*event.pos)
                        # TODO: Allow functions with less than two 
                        # parameters to be used.
                        func(x, y)

            # If the mouse moves and a button is down, call any associated
            # drag handlers
            elif event.type == MOUSEMOTION:
                for button in range(1, 6):
                    sprite = _clicked_sprite.get(button, None)
                    if sprite:
                        for func in sprite._drag_handlers.get(button, []):
                            x, y = _turtle_location(*event.pos)
                            # TODO: Allow functions with less than two 
                            # parameters to be used.
                            func(x, y)

        # Get a dictionary containing the state of the keyboard keys
        keys = pygame.key.get_pressed()

        # Loop through the keyhold handlers and call any for which the 
        # key is down
        try:
            for key_code, func in _keyhold_funcs.items():
                if key_code is None and keys.count(1) > 0:
                    func()
                elif key_code is not None and keys[key_code]:
                    func()
        except RuntimeError:
            pass

        # If the screen has changed, update the screen
        if _update_scheduled:
            _update()

    # Close the screen
    pygame.quit()


def onevent (func):
    '''
    Add an event handler function to be called when some custom event is posted.

    The argument is a function to be called when the event occurs.

    The function will return the code used for these events.
    '''

    global _custom_events

    # If this function has already been registered, use its previous event id
    if func in _custom_events:
        code = _custom_events.index(func) + USEREVENT

    # Otherwise, add the event to the custom events list and create its event
    # id
    else:
        code = len(_custom_events) + USEREVENT
        _custom_events.append(func)

    # Return the event code
    return code


def onkeyhold (func, key=None):
    '''
    Add an event handler function to be called repeatedly when a key is held 
    down.

    If the argument is `None`, then any currently assigned handlers are 
    removed.  Otherwise the given handler is assigned.  Any previously 
    assigned handler is replaced.

    The `key` argument is a string that represent the key.  If none is 
    provided, then this handler will be used for all keys that do not 
    explicitly have a handler set.
    '''

    if key is None:
        _keyhold_funcs[None] = func
    elif isinstance(key, str):
        _keyhold_funcs[pygame.key.key_code(key)] = func
    else:
        _keyhold_funcs[key] = func


def onkeypress (func, key=None):
    '''
    Add an event handler function to be called when a key is initially 
    pressed.

    If the argument is `None`, then any currently assigned handlers are 
    removed.  Otherwise the given handler is assigned.  Any previously 
    assigned handler is replaced.

    The `key` argument is a string that represent the key.  If none is 
    provided, then this handler will be used for all keys that do not 
    explicitly have a handler set.
    '''

    if key is None:
        _keypress_funcs[None] = func
    elif isinstance(key, str):
        _keypress_funcs[pygame.key.key_code(key)] = func
    else:
        _keypress_funcs[key] = func

def onkeyrelease (func, key=None):
    '''
    Add an event handler function to be called when a key is released.

    If the argument is `None`, then any currently assigned handlers are 
    removed.  Otherwise the given handler is assigned.  Any previously 
    assigned handler is replaced.

    The `key` argument is a string that represent the key.  If none is 
    provided, then this handler will be used for all keys that do not 
    explicitly have a handler set.
    '''

    if key is None:
        _keyrelease_funcs[None] = func
    elif isinstance(key, str):
        _keyrelease_funcs[pygame.key.key_code(key)] = func
    else:
        _keyrelease_funcs[key] = func


def onscreenclick (func, button=1, add=None):
    '''
    Add an event handler for click events on the screen.

    If given `None`, then all click event handlers are removed for that
    button.

    The `button` argument sets which mouse button on the mouse is used:
    * button=1 is the left mouse button
    * button=2 is the center mouse button
    * button=3 is the right mouse button
    * button=4 is scrolling the mouse scroller up
    * button=5 is scrolling the mouse scroller down

    If `add` is set to `False`, then all previously added handlers will
    removed.  Otherwise, this handler will replace the most previously
    added handler.
    '''

    # If None is given, remove all of the handlers
    if func is None:
        _screenclick_handlers.pop(button, None)

    # Otherwise, add the handler. 
    elif button in _screenclick_handlers:
        if add:
            _screenclick_handlers[button].append(func)
        else:
            # Replace the last handler added
            _screenclick_handlers[button][-1] = func
    else:
        _screenclick_handlers[button] = [func]


def ontimer (func, t=0, repeat=False):
    '''
    Add an event handler function to be called after a set period of time.

    The first argument is a function to be called when the timer expires.  The
    second argument is the number of milliseconds to set the timer for.

    If the `repeat` parameter is set to `True`, then the timer will restart
    automatically after each time that it expires.

    To disable a timer, call this function with a time of 0.

    The function will return the code used for these events.
    '''

    # Register the function as a custom event handler
    code = onevent(func)

    # Start the timer
    pygame.time.set_timer(code, t, not repeat)

    # Return the code
    return code


def radians ():
    '''
    Set the unit of measure for angles to radians.

    This will make a full rotation have an angle of 2 * pi.
    '''

    global _fullcircle

    _fullcircle = math.tau


def resetscreen ():
    '''
    Reset all of the turtles.
    '''

    for turt in _sprite_group:
        turt.reset()


def screensize (canvwidth=None, canvheight=None, bg=None):
    '''
    Get or change the size of the screen.

    If no arguments are given, then return the current dimensions of the 
    screen.  Otherwise, change the screen to be the dimensions given by the
    first two arguments.

    A third argument can be given to change the background color.  See 
    bgcolor() for details on the format of this argument.
    '''

    # If no arguments are given, then return the current dimensions
    if canvwidth is None:
        return _screen.get_size()

    # If only a width is given, only change the width
    elif canvheight is None:
        setup(canvwidth, _screen.get_height())

    # Otherwise, change the width and height
    else:
        setup(canvwidth, canvheight)

    # If a third argument is given, set the background color
    if bg is not None:
        bgcolor(bg)


def setup (width, height):
    '''
    Set up the screen.

    This function needs to be called at the start of your program or no
    screen will be created.
    '''

    global _screen

    # Create a screen
    _screen = pygame.display.set_mode((width, height))

    # If a background picture has been set, move it to the center of the
    # screen
    if _bgpic is not None:
        _bgpic_rect.centerx = _screen.get_width() / 2
        _bgpic_rect.centery = _screen.get_height() / 2


def title (titlestring):
    '''
    Set the title of the screen
    '''

    pygame.display.set_caption(titlestring)


def tracer (n=None, delay=None):
    '''
    This function does nothing.

    It is included for compatibility with the original turtle module.
    '''

    pass


def turtles ():
    '''
    Get a list of all the turtles created.
    '''
    return list(_sprite_group)


def update ():
    '''
    Update the screen.

    If the mainloop is not running, then this will update the screen
    immediately.

    If the mainloop is running, the screen will get updated on the next frame.
    '''

    global _update_scheduled

    # If the mainloop is running, flag that a screen update is needed
    if _running:
        _update_scheduled = True

    # If the mainloop is not running, do the update
    else:
        _update()


def window_height ():
    '''
    Get the height of the screen.
    '''

    return _screen.get_height()


def window_width ():
    '''
    Get the width of the screen.
    '''

    return _screen.get_width()

        

# This is all of the stuff that will be imported with 
# "from superturtle import *"
__all__ = [
    'Turtle', 'addshape', 'bgcolor', 'bgpic', 'bye', 
    'clearscreen', 'collections', 'colormode', 'degrees', 
    'delay', 'getshapes', 'listen', 'mainloop', 'math', 
    'onkeyhold', 'onkeypress', 'onkeyrelease', 'onscreenclick', 
    'ontimer', 'pygame', 'radians', 'resetscreen', 'screensize', 
    'setup', 'title', 'turtles', 'update', 'window_height', 
    'window_width'
]

