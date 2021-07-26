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

################################################################################
#                               GLOBAL VARIABLES
################################################################################

import math
import pygame

from screen import *
from sprite import *

################################################################################
#                                 COLOR CLASS
################################################################################

# We will provide the Color class from pygame directly.
from pygame import Color

################################################################################
#                                PAINTER CLASS
################################################################################

class Painter (Sprite):
    '''
    A Painter is a special sub-class of a Sprite with extra methods used to 
    draw on the screen.  All methods of a Sprite object can be used on
    Painter objects.

    Some features of Painter objects include:
     - They can draw on the screen when they move.
     - They can be used to draw filled polygons.
     - They can draw dots and circles.
     - They can stamp copies of their image to the screen.
     - They can write text to the screen.
    '''

    # A cache that stores fonts previously used.
    _fonts = {}

    def __init__ (self, image=None):
        '''
        Create a Painter object.

        An `image` may be provided:
         - The image can be the name of an image file.
         - If no image is provided, then the Painter will be a 1x1 pixel
           transparent sprite.
        '''

        Sprite.__init__(self, image)

        # Attributes associate with the painter's pen
        self._pendown = True
        self._pencolor = "black"
        self._pencolor_obj = Color("black")
        self._pensize = 1
        self._stepsize = 0.1

        # Attributes associates with fills
        self._filling = False
        self._fill_as_moving = None
        self._fillpoly = None
        self._fillcolor = "black"
        self._fillcolor_obj = Color("black")
        self._fill_canvas = None
        self._drawings_over_fill = None


    ### Color Methods

    def set_color (self, color):
        '''
        Change the pen color and fill color.

        The given `color` be one of the following values:
         - A valid color string.  See https://replit.com/@cjdevet/PygameColors
           to explore the available color strings.
         - A set of three numbers between 0 and 255 that represent the
           amount of red, green, blue to use in the color.  A fourth transparency
           value can be added.
         - An HTML color code in the form "#rrggbb" where each character 
           r, g, b and a are replaced with a hexidecimal digit.  For translucent
           colors, add another pair of hex digits ("##rrggbbaa").
         - An integer that, when converted to hexidecimal, gives an HTML color
           code in the form 0xrrggbbaa.
         - A pygame Color object.
        '''

        self._pencolor_obj = Color(color)
        self._pencolor = color
        self._fillcolor_obj = Color(color)
        self._fillcolor = color


    def get_colors (self):
        '''
        Returns a tuple containing the current pen color and fill color.
        '''

        return self._pencolor, self._fillcolor


    def set_pen_color (self, color):
        '''
        Change the pen color.

        See `Painter.set_color()` for values of `color`.
        '''

        self._pencolor_obj = Color(color)
        self._pencolor = color


    def get_pen_color (self):
        '''
        Returns the current pen color.
        '''

        return self._pencolor


    def set_fill_color (self, color):
        '''
        Change the fill color.

        See `Painter.set_color()` for values of `color`.
        '''

        self._fillcolor_obj = Color(color)
        self._fillcolor = color

    
    def get_fill_color (self):
        '''
        Returns the current fill color.
        '''

        return self._fillcolor


    ### Drawing Pen Methods

    def set_pen_width (self, width):
        '''
        Sets the width of the pen used to draw lines.
        '''

        if width < 1:
            raise ValueError("The width must be a positive integer.")
        self._pensize = int(width)


    def get_pen_width (self):
        '''
        Returns the current width of the pen used to draw lines.
        '''

        return self._pensize


    def set_step_size (self, distance):
        '''
        Change the step size between points drawn on a line.

        By default, the step size is 0.1 pixels.
        '''

        if distance <= 0:
            raise ValueError("The step size must be a positive number.")
        self._stepsize = distance


    def get_step_size (self):
        '''
        Returns the step size between points drawn on a line.
        '''

        return self._stepsize


    def put_pen_down (self):
        '''
        Put the pen on the screen and start drawing.
        '''

        self._pendown = True


    def pick_pen_up (self):
        '''
        Pick the pen up off the screen and stop drawing.
        '''

        self._pendown = False


    def is_pen_down (self):
        '''
        Return whether or not the pen is on the screen and is drawing.
        '''

        return self._pendown


    ### Drawing Methods

    # A helper method that draws a line from start to end on the given canvas.
    def _draw_line (self, start, end, canvas=None):
        if canvas is None:
            # Get the active screen's canvas
            screen = get_active_screen()
            if screen is None:
                raise RuntimeError("Can't draw a line on an inactive screen!")
            if self not in screen:
                raise RuntimeError("The painter must be on the active screen to draw!")
            canvas = screen.get_canvas()

        # Convert to pygame coordinates
        start = to_pygame_coordinates(start)
        end = to_pygame_coordinates(end)

        # If width is 1, use the pygame function
        if self._pensize == 1:
            pygame.draw.line(canvas, self._pencolor_obj, start, end)

        # Otherwise use dots instead
        else:
            # Find geometric properties of the line
            delta = end - start
            distance, direction = delta.as_polar()

            # Draw dots every 0.1 pixels along the line between the points
            radius = self._pensize / 2
            current = start
            delta = pygame.Vector2(self._stepsize, 0).rotate(direction)
            for _ in range(int(distance / self._stepsize) + 1):
                pygame.draw.circle(canvas, self._pencolor_obj, current, radius)
                current += delta

    def set_position (self, x, y=None):
        '''
        Move the Sprite to the given coordinates and, is the pen is down, draw a
        line.
        '''

        # If only on argument is given, expand it into two
        if y is None:
            x, y = x

        # Actually move the sprite and get the start and end points
        start = self._pos
        Sprite.set_position(self, x, y)

        # If the turtle is currently creating a filled shape, add the point to the
        # list of filled polygon points and draw the line on the upper layer
        # to be drawn on top of the fill.
        if self._filling:
            self._fillpoly.append(self._pos)
            self._draw_line(start, self._pos, self._drawings_over_fill)

        # Draw the line
        if self._pendown:
            self._draw_line(start, self._pos)


    def walk_path (self, path):
        '''
        Move the Sprite along a path and, is the pen is down, draw a line.

        The path should be a list of coordinate pairs
        (e.g. `[(100, 0), (-200, 100), (200, -50)]`)
        '''

        # Call .set_position() on each point in the path
        for point in path:
            self.set_position(point)


    ### Creating Filled Shapes

    # A helper method that draws the current filled polygon on the given canvas.
    def _draw_fill (self, canvas=None):
        # If no canvas is provided, use the active screen's
        if canvas is None:
            screen = get_active_screen()
            if screen is None:
                raise RuntimeError("Can't draw a filled shape on an inactive screen!")
            if self not in screen:
                raise RuntimeError("The painter must be on the active screen to draw!")
            canvas = screen.get_canvas()

        # Draw the points to the canvas
        points = [to_pygame_coordinates(p) for p in self._fillpoly]
        if len(points) >= 3:
            pygame.draw.polygon(canvas, self._fillcolor, points)

        # Draw the lines back on top of the canvas
        canvas.blit(self._drawings_over_fill, (0, 0))


    def begin_fill (self, as_moving=False):
        '''
        Start creating a filled shape.

        This function must be followed with a call to end_fill() which
        will draw the filled shape using all of the points visited
        from the call of this method.

        If `as_moving` is set to `True`, then the filled shape will be redrawn
        after each move of the sprite.
        '''

        # Set the fill properties
        self._filling = True
        self._fillpoly = [self._pos]
        self._fill_as_moving = bool(as_moving)

        # Create a surface to hold the lines drawn on top of the fill
        screen = get_active_screen()
        if screen is None:
            raise RuntimeError("Can't draw a filled shape on an inactive screen!")
        if self not in screen:
            raise RuntimeError("The painter must be on the active screen to draw!")
        self._drawings_over_fill = pygame.Surface(screen.get_size(), pygame.SRCALPHA)


    def end_fill (self):
        '''
        Complete drawing a filled shape.

        This function must be preceded by a call to begin_fill().  When
        this method is called, a filled shape will be drawn using all of the
        points visited since begin_fill() was called.
        '''

        # If .begin_fill() wasn't called, just do nothing.
        if not self._filling:
            return

        # Draw the filled shape on the active screen
        self._draw_fill()
        
        # Reset the filling attributes
        self._filling = False
        self._fillpoly = None


    def is_filling (self):
        '''
        Returns whether or not a filled shape is currently being drawn.
        '''

        return self._filling


    ### Draw circles

    def dot (self, size=None, color=None):
        '''
        Draw a dot.

        The dot will be centered at the current position and have diameter
        `size`.  If no size is given a dot slightly larger than the pen width
        will be drawn.

        If the `color` is not specified, the pen color is used.
        '''

        # Get the active screen's canvas
        screen = get_active_screen()
        if screen is None:
            raise RuntimeError("Can't draw a dot on an inactive screen!")
        if self not in screen:
            raise RuntimeError("The painter must be on the active screen to draw!")
        canvas = screen.get_canvas()

        # If no size is given, make the dot a bit bigger than the pen size
        if size is None:
            size = max(self._pensize + 4, 2 * self._pensize)

        # If no color is given use the pen color
        if color is None:
            color = self._pencolor_obj

        # Draw the dot
        point = to_pygame_coordinates(self._pos)
        pygame.draw.circle(canvas, color, point, size / 2)

        # If the turtle is currently creating a filled shape, draw the dot on 
        # the upper layer to be drawn on top of the fill.
        if self._filling:
            pygame.draw.circle(self._drawings_over_fill, color, point, size / 2)


    def circle (self, radius, extent=None):
        '''
        Draw a circle counterclockwise.

        The circle will have the given `radius`.  If `radius` is negative, then
        the circle is draw clockwise.
        
        The `extent` is used to draw an arc around a portion of a circle.  If 
        `extent` is negative, draw the circle clockwise.

        The circle will actually be an approximation.  The turtle will really
        draw a regular polygon with 360 sides.
        '''

        # Because the circle is an approximation, we will calculate the
        # final position and set it after the circle is drawn.
        if extent % 360 == 0:
            end = self._pos
        else:
            delta = pygame.Vector2(0, -radius)
            delta.rotate_ip(extent if radius >= 0 else -extent)
            delta += pygame.Vector2(0, radius)
            delta.rotate_ip(self._dir)
            end = self._pos + delta

        # Sanitize extent argument
        if extent is None:
            extent = 360
        else:
            extent = int(extent)

        # Set up the number of steps and the turn angle needed between
        # steps.
        step_size = abs(radius) * 2 * math.pi / 360
        turn_size = 1 if radius >= 0 else -1

        # Repeatedly move and turn to approximate the circle
        if extent > 0:
            for _ in range(extent):
                self.move_forward(step_size)
                self.turn_left(turn_size)
        else:
            for _ in range(-extent):
                self.turn_right(turn_size)
                self.move_backward(step_size)

        # Set the position to the one calculated above
        self._pos = end


    ### Draw a stamp

    def stamp (self):
        '''
        Stamp a copy of the sprite's image to the screen at the current position.
        '''

        # Get the active screen's canvas
        screen = get_active_screen()
        if screen is None:
            raise RuntimeError("Can't stamp an image on an inactive screen!")
        if self not in screen:
            raise RuntimeError("The painter must be on the active screen to draw!")
        canvas = screen.get_canvas()

        # Copy the image to the canvas
        self._clean_image()
        canvas.blit(self.image, self.rect)

        # If the turtle is currently creating a filled shape, stamp the image on 
        # the upper layer to be drawn on top of the fill.
        if self._filling:
            self._drawings_over_fill.blit(self.image, self.rect)


    ### Write on the screen

    def write (self, text, align="middle center", font="Arial", font_size=12, font_style=None):
        '''
        Write text to the screen at the turtle's current location using the pen.

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

        # If font is a Font object, just use that
        if isinstance(font, pygame.font.Font):
            font_obj = font

        # If this font and size have been used before, check the _fonts cache
        if (font, font_size) in Painter._fonts:
            font_obj = Painter._fonts[font, font_size]

        # If the font ends in ".ttf", then load the font from the file
        elif font.endswith(".ttf"):
            font_obj = pygame.font.Font(font, font_size)
            Painter._fonts[font, font_size] = font_obj

        # Otherwise, use a system font
        else:
            font_obj = pygame.font.SysFont(font, font_size)
            Painter._fonts[font, font_size] = font_obj

        # Apply the styles
        if font_style is not None:
            if isinstance(font_style, str):
                font_style = font_style.split()
            font_style = [style.lower() for style in font_style]
            font_obj.set_bold("bold" in font_style)
            font_obj.set_italic("italic" in font_style)
            font_obj.set_underline("underline" in font_style)

        # Render an image of the text
        image = font_obj.render(str(text), True, self._pencolor)
        rect = image.get_rect()

        # Set the position of the text from the align parameter
        if isinstance(align, str):
            align = align.split()
        align = [location.lower() for location in align]
        x, y = to_pygame_coordinates(self._pos)
        rect.centerx = x
        rect.centery = y
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
        screen = get_active_screen()
        if screen is None:
            raise RuntimeError("Can't write text on an inactive screen!")
        if self not in screen:
            raise RuntimeError("The painter must be on the active screen to draw!")
        canvas = screen.get_canvas()
        canvas.blit(image, rect)

        # Return a Font object that can be used for future writing
        return font_obj


    ### Override the Sprite update() method

    def update (self, screen=None):
        '''
        Update the sprite in preparation to draw the next frame.

        This method should generally not be called explicitly, but will be called
        by the event loop if the sprite is on the active screen.
        '''

        Sprite.update(self, screen)

        # If filling while moving, include the fill-so-far on the screen.
        if screen is None:
            screen = get_active_screen()
        if (screen is not None and self in screen and self._filling and
                self._fill_as_moving):
            self._draw_fill(screen._update_drawings)


# What is included when importing *
__all__ = [
    "Painter",
    "Color"
]
