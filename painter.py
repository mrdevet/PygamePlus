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
#                              MODULE DESCRIPTION
################################################################################

"""
TODO
"""

################################################################################
#                               GLOBAL VARIABLES
################################################################################

import math
import pygame
from pygame import Color

from screen import get_active_screen, to_pygame_coordinates
from sprite import *

################################################################################
#                                 SPRITE CLASS
################################################################################

class Painter (Sprite):

    # A cache that stores fonts previously used.
    _fonts = {}

    def __init__ (self, image_file=None):
        Sprite.__init__(self, image_file)
        self._pendown = True
        self._pencolor = "black"
        self._pencolor_obj = pygame.Color("black")
        self._pensize = 1
        self._stepsize = 0.1
        self._filling = False
        self._fill_as_moving = None
        self._fillpoly = None
        self._fillcolor = "black"
        self._fillcolor_obj = pygame.Color("black")
        self._fill_canvas = None
        self._drawings_over_fill = None

    # Set and get colors

    def set_color (self, color):
        self._pencolor_obj = Color(color)
        self._pencolor = color
        self._fillcolor_obj = Color(color)
        self._fillcolor = color

    def get_colors (self):
        return self._pencolor, self._fillcolor

    def set_pen_color (self, color):
        self._pencolor_obj = Color(color)
        self._pencolor = color

    def get_pen_color (self):
        return self._pencolor

    def set_fill_color (self, color):
        self._fillcolor_obj = Color(color)
        self._fillcolor = color
    
    def get_fill_color (self):
        return self._fillcolor

    def set_pen_width (self, width):
        self._pensize = width

    def get_pen_width (self):
        return self._pensize

    def set_step_size (self, distance):
        self._stepsize = distance

    def get_step_size (self, distance):
        return self._stepsize

    def put_pen_down (self):
        self._pendown = True

    def pick_pen_up (self):
        self._pendown = False

    def is_pen_down (self):
        return self._pendown

    # Draw on movement

    def _draw_line (self, start, end, canvas=None):
        if canvas is None:
            # Get the active screen's canvas
            screen = get_active_screen()
            if screen is None:
                return
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
            for _ in range(int(distance / self._stepsize)):
                pygame.draw.circle(canvas, self._pencolor_obj, current, radius)
                current += delta
            pygame.draw.circle(canvas, self._pencolor_obj, current, radius)

    def set_position (self, x, y=None):
        if y is None:
            x, y = x

        # Actually move the sprite
        start = self._pos
        Sprite.set_position(self, x, y)            

        # If the turtle is currently creating a filled shape, store
        # the point.
        if self._filling:
            self._fillpoly.append(self._pos)
            self._draw_line(start, self._pos, self._drawings_over_fill)

        # Draw the line
        if self._pendown:
            self._draw_line(start, self._pos)

    def walk_path (self, path):
        for point in path:
            self.set_position(point)

    ### Creating Filled Shapes

    def _draw_fill (self, canvas=None):
        if canvas is None:
            # Get the active screen's canvas
            screen = get_active_screen()
            if screen is None:
                return
            canvas = screen.get_canvas()

        # Draw the points to the canvas
        points = [to_pygame_coordinates(p) for p in self._fillpoly]
        if len(points) >= 3:
            pygame.draw.polygon(canvas, self._fillcolor, points)

        # Draw the lines back on top of the canvas
        canvas.blit(self._drawings_over_fill, (0, 0))

    def begin_fill (self, as_moving=False):
        self._filling = True
        self._fillpoly = [self._pos]
        self._fill_as_moving = bool(as_moving)
        screen = get_active_screen()
        self._drawings_over_fill = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    def end_fill (self):
        '''
        Complete drawing a filled shape.

        This function must be preceded by a call to begin_fill().  When
        this method is called, a filled shape will be drawn using all of the
        points visited since begin_fill() was called.
        '''

        if not self._filling:
            return

        self._draw_fill()
        
        # Reset the filling attributes
        self._filling = False
        self._fillpoly = None

    def is_filling (self):
        return self._filling

    ### Draw circles

    def dot (self, size=None, color=None):
        '''
        Draw a dot.

        The dot will be centered at the current position and have diameter
        `size`.

        If the `color` is not specified, the pen color is used.
        '''

        # Get the active screen's canvas
        screen = get_active_screen()
        if screen is None:
            return
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

        if self._filling:
            pygame.draw.circle(self._drawings_over_fill, color, point, size / 2)

    def circle (self, radius, extent=None):
        '''
        Draw a circle counterclockwise.

        The circle will have the given `radius`.  The `extent` is used to
        draw an arc around a portion of a circle.  If extent is negative,
        draw the circle clockwise.

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

        # Repeatedly move forward and turn to approximate the circle
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
        # Get the active screen's canvas
        screen = get_active_screen()
        if screen is None:
            return
        canvas = screen.get_canvas()

        # Copy the image to the canvas
        self._clean_image()
        canvas.blit(self.image, self.rect)

        if self._filling:
            self._drawings_over_fill.blit(self.image, self.rect)

    ### Write on the screen

    def write (self, text, align="middle center", font="Arial", font_size=8, font_style="normal"):
        '''
        Write text to the screen at the turtle's current location.

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
            return
        canvas = screen.get_canvas()
        canvas.blit(image, rect)

        # Return a Font object that can be used for future writing
        return font_obj



    def update (self, screen=None):
        Sprite.update(self, screen)

        if screen is None:
            screen = get_active_screen()
        if screen is not None and self._filling and self._fill_as_moving:
            self._draw_fill(screen._surface)


        

__all__ = [
    "Painter",
    "Color"
]
