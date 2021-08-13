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

import pgputils
from screen import get_active_screen, to_pygame_coordinates

################################################################################
#                                 SPRITE CLASS
################################################################################

class Sprite (pygame.sprite.Sprite):
    '''
    A Sprite represents an image that moves around the screen in a game.

    Sprite objects store the following information necessary for drawing these
    images on the screen:
     - The position of the sprite on the screen using coordinates
     - The direction that the sprite is pointing using an angle measured
       counterclockwise from the positive x-axis.

    Methods are provided for the following:
     - Moving and turning the sprite
     - Detecting whether or not a sprite is touching other sprites
     - Animating the sprite
     - Adding behaviour when the mouse interacts with the sprite
    '''

    def __init__ (self, image=None):
        '''
        Create a Painter object.

        An `image` may be provided:
         - The image can be the name of an image file.
         - It can also be a list of points that create a polygon.
         - If no image is provided, then the Painter will be a 1x1 pixel
           transparent sprite.
        '''

        pygame.sprite.Sprite.__init__(self)

        # Handle the image
        if image is None:
            self._original = pygame.Surface((1, 1), pygame.SRCALPHA)
        elif isinstance(image, str):
            if image in pgputils.polygon_images:
                self._original = pgputils.polygon_images[image]
            else:
                self._original = pygame.image.load(image).convert_alpha()
        elif isinstance(image, tuple) or isinstance(image, list):
            self._original = tuple([pygame.Vector2(p) for p in image])
        elif isinstance(image, pygame.Surface):
            self._original = image
        else:
            raise ValueError("Invalid image!")

        # The .image and .rect attributes are needed for drawing sprites
        # in a pygame group
        if isinstance(self._original, tuple):
            self.image = pgputils.polygon_to_surface(self._original, "black", "black")
        else:
            self.image = self._original
        self._scaled = self._original
        self._rotated = self._scaled
        self.rect = self.image.get_rect()

        # Positional and directional attributes
        self._pos = pygame.Vector2(0, 0)
        self._dir = 0
        self._move_ratio = pygame.Vector2(1, 0)

        # Scale and rotation attributes
        self._scale = pygame.Vector2(1, 1)
        self._dirty_scale = False
        self._smooth = False
        self._rotates = False
        self._tilt = 0
        self._dirty_rotate = False
        self._dirty_mask = True

        # Attributes for lines and fill of polygon images
        self._linecolor = "black"
        self._linecolor_obj = pygame.Color("black")
        self._linesize = 1
        self._fillcolor = "black"
        self._fillcolor_obj = pygame.Color("black")

        # Attributes that hold any event handlers associated with the sprite
        self._on_update_func = None
        self._click_funcs = [None for _ in range(5)]
        self._release_funcs = [None for _ in range(5)]
        self._drag_funcs = [None for _ in range(5)]


    ### Visibility Methods

    def show (self):
        active_screen = get_active_screen()
        if active_screen is not None:
            self.add(active_screen)

    def hide (self):
        active_screen = get_active_screen()
        if active_screen is not None:
            self.remove(active_screen)

    def is_visible (self):
        active_screen = get_active_screen()
        return active_screen is not None and self in active_screen


    ### Position Methods

    def set_position (self, x, y=None):
        '''
        Change the position of the sprite on the screen.

        The position is a pair of coordinates (x and y) which represent the
        distance that the sprite is from the center of the screen.  That is,
        the center of the screen is (0, 0) and the x-coordinate and y-coordinate 
        represent respectively how far horizontally and vertically the sprite is 
        from there.  Think of the screen as the traditional 2D coordinate plane
        used in mathematics.
        '''

        self._pos = pygame.Vector2(x, y)


    def go_to (self, x, y=None, turn=True):
        '''
        Move the sprite to the given coordinates.

        Unlike set_position(), this method will also turn the sprite in the 
        direction of the given location.  This behaviour can be turned of by
        setting the `turn` argument to `False`.
        '''

        if turn:
            # Get the distance and direction
            delta = pygame.Vector2(x, y) - self._pos
            distance, direction = delta.as_polar()

            # Don't turn if the sprite isn't moving
            if distance > 0:
                # Adjust direction to turn in closest direction
                if direction - self._dir > 180:
                    direction -= 360
                if direction - self._dir < -180:
                    direction += 360

                # Do the turn
                self.set_direction(direction)

        # Move the sprite
        self.set_position(x, y)


    def get_position (self):
        '''
        Return the current the position of the sprite on the screen.
        '''

        return tuple(self._pos)


    def set_x (self, x):
        '''
        Change the x-coordinate of the sprite's position on the screen.
        '''

        self.set_position(x, self._pos.y)


    def get_x (self):
        '''
        Returns the current x-coordinate of the sprite's position on the screen.
        '''

        return self._pos.x


    def set_y (self, y):
        '''
        Change the y-coordinate of the sprite's position on the screen.
        '''

        self.set_position(self._pos.x, y)


    def get_y (self):
        '''
        Returns the current y-coordinate of the sprite's position on the screen.
        '''

        return self._pos.y


    ### Direction Methods

    def set_direction (self, direction):
        '''
        Change the direction that the sprite is pointing.

        The direction is an angle (in degrees) counterclockwise from the 
        positive x-axis.  Here are some important directions:
         - 0 degrees is directly to the right
         - 90 degrees is directly up
         - 180 degrees is directly to the left
         - 270 degrees is directly down
        '''

        self._dir = direction

        # Ensure that the direction is between 0 and 360
        self._dir %= 360

        # Create a 2D vector that contains the amount that the x-coordinate 
        # and y-coordinate change if the sprite moves forward 1 pixel in this
        # direction
        self._move_ratio = pygame.Vector2(1, 0).rotate(self._dir)

        # If the image rotates, then flag that we need to update the image
        if self._rotates:
            self._dirty_rotate = True


    def turn_to (self, direction):
        '''
        Alias for set_direction().
        '''

        self.set_direction(direction)


    def get_direction (self):
        '''
        Return the current direction that the sprite is pointing.
        '''

        return self._dir

        
    def turn_left (self, angle):
        '''
        Turn the sprite left (counterclockwise) by the given `angle`.
        '''

        self.set_direction(self._dir + angle)


    def turn_right (self, angle):
        '''
        Turn the sprite right (clockwise) by the given `angle`.
        '''

        self.set_direction(self._dir - angle)


    ### Movement Methods

    def move_forward (self, distance):
        '''
        Move the sprite by the given `distance` in the direction it is currently
        pointing.
        '''

        self.set_position(self._pos + distance * self._move_ratio)


    def move_backward (self, distance):
        '''
        Move the sprite by the given `distance` in the opposite of the 
        direction it is currently pointing.
        '''

        self.set_position(self._pos - distance * self._move_ratio)

    
    ### Scaling and Rotating Image Methods

    def scale (self, factor):
        '''
        Scale the size of the image by the given `factor`.

        If `factor` is greater than 1, then the image is enlarged by multiplying
        its original dimensions by that number.  If `factor` is less than 1, then 
        the image is shrunk by multiplying its original dimensions by that 
        number.  If `factor` equals 1, then the image is scaled to its original 
        size.
        '''

        self._scale.x = factor
        self._scale.y = factor

        # Flag that the image may have been scaled and needs to be updated
        self._dirty_scale = True
        self._dirty_mask = True


    def scale_width (self, factor):
        '''
        Scale the width of the image by the given `factor`.

        This will scale the width of the original image before any rotation is
        applied.
        '''

        self._scale.x = factor

        # Flag that the image may have been scaled and needs to be updated
        self._dirty_scale = True
        self._dirty_mask = True


    def scale_height (self, factor):
        '''
        Scale the height of the image by the given `factor`.

        This will scale the height of the original image before any rotation is
        applied.
        '''

        self._scale.y = factor

        # Flag that the image may have been scaled and needs to be updated
        self._dirty_scale = True
        self._dirty_mask = True


    def set_image_rotates (self, rotates=True):
        '''
        Changes whether or not the image rotates when the sprite changes
        direction.

        Calling this method with no argument will turn on image rotation.  You 
        can also pass a boolean value to explicitly specify whether the image
        should rotate or not.
        '''

        self._rotates = rotates

        # Flag that the image may have rotated and needs to be updated
        self._dirty_rotate = True
        self._dirty_mask = True


    def get_image_rotates (self):
        '''
        Returns whether or not the image rotates when the sprite changes
        direction.
        '''

        return self._rotates


    def set_image_tilt (self, angle):
        '''
        Set the angle that the image is tilted.

        The `angle` is a counterclockwise if positive and clockwise if negative.

        If image rotation is off, then the image will stay tilted at this angle
        no matter what direction the sprite is pointing.  If image rotation is on,
        then the image will stay tilted at this angle relative to the sprite's
        direction.
        '''

        self._tilt = angle

        # Ensure that the angle is between 0 and 360
        self._tilt %= 360

        # Flag that the image may have rotated and needs to be updated
        self._dirty_rotate = True
        self._dirty_mask = True

    
    def get_image_tilt (self):
        '''
        Return the angle that the image is tilted.
        '''

        return self._tilt


    def use_smoothing (self, smooth=True):
        '''
        Set that images should be smoothed when scaled or rotated.

        Calling this method with no argument will turn on smoothing.  You can
        also pass a boolean value to explicitly turn on or off smoothing.

        By default, a quick and simple scale and rotation is applied.  This can 
        cause images to be pixelated (when enlarged), loose detail (when shrunk),
        or be distorted (when rotating).  If you set `smooth` to be `True`, then 
        each new pixel will be sampled and an average color will be used.  This 
        makes to scaled and rotated images be more smooth, but takes longer.  You 
        may want to avoid smooth scaling if you will be scaling or rotating the 
        image very frequently.
        '''

        self._smooth = smooth


    def is_smoothing (self):
        '''
        Returns whether or not smoothing is turned on.
        '''

        return self._smooth


    ### Color and Width Methods for Polygons

    def set_color (self, color):
        '''
        Change the line color and fill color.

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

        self._linecolor_obj = pygame.Color(color)
        self._linecolor = color
        self._fillcolor_obj = pygame.Color(color)
        self._fillcolor = color

        if isinstance(self._original, tuple):
            self._dirty_rotate = True


    def get_colors (self):
        '''
        Returns a tuple containing the current line color and fill color.
        '''

        return self._linecolor, self._fillcolor


    def set_line_color (self, color):
        '''
        Change the line color.

        See `Painter.set_color()` for values of `color`.
        '''

        self._linecolor_obj = pygame.Color(color)
        self._linecolor = color

        if isinstance(self._original, tuple):
            self._dirty_rotate = True


    def get_line_color (self):
        '''
        Returns the current line color.
        '''

        return self._linecolor


    def set_fill_color (self, color):
        '''
        Change the fill color.

        See `Painter.set_color()` for values of `color`.
        '''

        self._fillcolor_obj = pygame.Color(color)
        self._fillcolor = color

        if isinstance(self._original, tuple):
            self._dirty_rotate = True

    
    def get_fill_color (self):
        '''
        Returns the current fill color.
        '''

        return self._fillcolor


    ### Update Method

    # Helper method that scales and/or rotates the image if it is dirty    
    def _clean_image (self):
        # If the image is a polygon, scale and rotate the points before drawing it
        if isinstance(self._original, tuple):
            if self._dirty_scale:
                self._scaled = tuple([self._scale.elementwise() * p for p in 
                                      self._original])
                self._dirty_rotate = True
                self._dirty_scale = False
            
            if self._dirty_rotate:
                angle = self._dir + self._tilt if self._rotates else self._tilt
                self._rotated = tuple([p.rotate(angle) for p in self._scaled])
                self._dirty_rotate = False
                self.image = pgputils.polygon_to_surface(self._rotated, 
                                self._linecolor,
                                self._fillcolor,
                                round((self._scale.x + self._scale.y) // 2))

        # Otherwise, scale and rotate the surfaces
        else:
            if self._dirty_scale:
                orig_width, orig_height = self._original.get_size()
                new_width = round(self._scale.x * orig_width)
                new_height = round(self._scale.y * orig_height)
                if self._smooth:
                    self._scaled = pygame.transform.smoothscale(
                            self._original, (new_width, new_height))
                else:
                    self._scaled = pygame.transform.scale(
                            self._original, (new_width, new_height))
                self._dirty_rotate = True
                self._dirty_scale = False

            if self._dirty_rotate:
                angle = self._dir + self._tilt if self._rotates else self._tilt
                if self._smooth:
                    self._rotated = pygame.transform.rotozoom(self._scaled, angle, 1)
                else:
                    self._rotated = pygame.transform.rotate(self._scaled, angle)
                self.image = self._rotated
                self._dirty_rotate = False

    # Helper method that determines the image's mask if it is dirty
    def _clean_mask (self):
        if self._dirty_mask:
            self.mask = pygame.mask.from_surface(self.image)
            self._dirty_mask = False


    def update (self, screen=None):
        '''
        Update the sprite in preparation to draw the next frame.

        This method should generally not be called explicitly, but will be called
        by the event loop if the sprite is on the active screen.
        '''

        # If a custom update function has been applied, call it
        if self._on_update_func is not None:
            pgputils.call_with_args(self._on_update_func, sprite=self)

        # Update the sprite's .image and .rect attributes needed for drawing
        self._clean_image()
        self.rect = self.image.get_rect() 
        if screen is None:
            self.rect.center = to_pygame_coordinates(self._pos)
        else:
            self.rect.center = screen.to_pygame_coordinates(self._pos)


    ### Other Sprite Methods

    def get_distance_to (self, other):
        '''
        Return the distance this sprite is away from another.
        '''

        return self._pos.distance_to(other._pos)


    def get_direction_to (self, other):
        '''
        Return the angle that this sprite must turn toward to be pointing 
        directly at another.
        '''

        return pygame.Vector2(1, 0).angle_to(other._pos - self._pos)


    ### Collision Methods

    def is_touching_point (self, x, y=None, method="rect"):
        '''
        Returns whether or not the sprite is touching a given point.

        The `method` argument can be used to specify which type of collision
        detection to use:
         - The "rect" method will determine if the point is inside of the rectangle
           that the image is contained in.  This is the default.
         - The "circle" method will determine if the point is inside of a circle
           centered at the sprite's position.  To use circle collision, you need
           to specify a `.radius` attribute for the sprite or the circle will be the
           smallest circle that encloses the entire image.
         - The "mask" method will determine if the point is touching a 
           non-transparent part of the image.
         - You can pass in a custom function that takes two sprites as arguments
           and returns a Boolean value indicating if they are touching.
        '''

        # If this sprite isn't visible, then it can't be in collision
        if not self.is_visible():
            return False

        # Get the collision detection function for the given method
        if isinstance(method, str):
            if method not in pgputils.collision_functions:
                raise ValueError(f"Invalid collision method: {method}")
            method = pgputils.collision_functions[method]

        # Create the other "sprite"
        if y is None:
            x, y = x
        other_sprite = pygame.sprite.Sprite()
        pygame_x, pygame_y = to_pygame_coordinates(x, y)
        other_sprite.rect = pygame.Rect(pygame_x, pygame_y, 1, 1)
        other_sprite.radius = 0.5
        other_sprite.mask = pygame.mask.Mask((1, 1), True)

        # Update the turtle and, if dirty, get its mask
        self._clean_image()
        if method == pygame.sprite.collide_mask:
            self._clean_mask()

        # Collision detection if given a point
        return bool(method(self, other_sprite))


    def get_touching (self, others, method="rect"):
        '''
        Takes a collection of sprites and returns the subset that the sprite is
        touching.

        See the Sprite.is_touching() method for details on the `method` parameter.
        '''

        # If this sprite isn't visible, then it can't be in collision
        if not self.is_visible():
            return False

        # Get the collision detection function for the given method
        if isinstance(method, str):
            if method not in pgputils.collision_functions:
                raise ValueError(f"Invalid collision method: {method}")
            method = pgputils.collision_functions[method]

        # Update the turtle and, if dirty, get its mask
        self._clean_image()
        if method == pygame.sprite.collide_mask:
            self._clean_mask()

        # If given a list, loop through it use the method from above
        if isinstance(other, list):
            hit_list = []
            for other_sprite in other:
                other_sprite._clean_image()
                if method == pygame.sprite.collide_mask:
                    other_sprite._clean_mask()
                if other in active_screen and bool(method(self, other_sprite)):
                    hit_list.append(other)
            return hit_list
        
        # If given a pygame sprite group, use the pygame function for 
        # collision detection with a group
        elif isinstance(other, pygame.sprite.Group):
            other.update()
            hit_list = pygame.sprite.spritecollide(self, other, False, method)
            return hit_list

        # If given an invalid argument, just return False
        else:
            return ValueError("Invalid argument!")


    def is_touching (self, other, method="rect"):
        '''
        Returns whether or not the sprite is touching another sprite (or 
        collection of sprites).

        The `method` argument can be used to specify which type of collision
        detection to use:
         - The "rect" method will determine if the rectangles that the images are 
           contained in are overlapping.  This is the default.
         - The "circle" method will determine if circles centered at the sprites' 
           positions are overlapping.  To use circle collision, you need to 
           specify a `.radius` attribute for the sprites or the circle will be 
           the smallest circle that encloses the entire image.
         - The "mask" method will determine if the non-transparent parts of the 
           images are overlapping.
         - You can pass in a custom function that takes two sprites as arguments
           and returns a Boolean value indicating if they are touching.
        '''

        # If this sprite isn't visible, then it can't be in collision
        if not self.is_visible():
            return False

        active_screen = get_active_screen()

        # Get the collision detection function for the given method
        if isinstance(method, str):
            if method not in pgputils.collision_functions:
                raise ValueError(f"Invalid collision method: {method}")
            method = pgputils.collision_functions[method]

        # Update the turtle and, if dirty, get its mask
        self._clean_image()
        if method == pygame.sprite.collide_mask:
            self._clean_mask()

        # If given just a sprite, put it into a list
        if isinstance(other, pygame.sprite.Sprite):
            other._clean_image()
            if method == pygame.sprite.collide_mask:
                other._clean_mask()
            return other in active_screen and bool(method(self, other))

        # If given a list, loop through it use the method from above
        elif isinstance(other, list):
            for other_sprite in other:
                other_sprite._clean_image()
                if method == pygame.sprite.collide_mask:
                    other_sprite._clean_mask()
                if other in active_screen and bool(method(self, other_sprite)):
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
            return ValueError("Invalid argument!")


    ### Add Custom Update Function

    def on_update (self, func):
        '''
        Add a custom update function that will be called on every iteration of
        the event loop.
        
        You can provide the following arguments for the function `func`:
         - `sprite` - will provide the sprite object being updated
        '''

        self._on_update_func = func


    ### Click Event Methods

    def on_click (self, func, button="left"):
        '''
        Add a function that will be called when the mouse is clicked on
        this sprite.

        You can provide the following arguments for the function `func`:
         - `x` - will provide x-coordinate of the mouse
         - `y` - will provide y-coordinate of the mouse
         - `pos` - will provide a tuple of the coordinates (x and y) of the mouse
         - `button` - will provide the name of the mouse button used
         - `sprite` - will provide the sprite object involved

        You can specify which mouse button needs to be used for the click using
        the `button` parameter.  It's value needs to be one of "left", "center", 
        "right", "scrollup" or "scrolldown".  The left button is the default.
        '''

        # TODO: Add ability to only have click events when mask clicked on.
        #   This could make use of the is_touching_point() method

        # Convert the button string to a button number
        if isinstance(button, str):
            try:
                button = pgputils.mouse_button_map[button]
            except KeyError:
                raise ValueError("Invalid button!")

        # If a button is valid, add the function to the appropriate button
        if 1 <= button <= 5:
            self._click_funcs[button - 1] = func
        else:
            raise ValueError("Invalid button!")


    def on_release (self, func, button="left"):
        '''
        Add a function that will be called when the mouse is released after 
        clicking on this sprite.

        You can provide the following arguments for the function `func`:
         - `x` - will provide x-coordinate of the mouse
         - `y` - will provide y-coordinate of the mouse
         - `pos` - will provide a tuple of the coordinates (x and y) of the mouse
         - `button` - will provide the name of the mouse button used
         - `sprite` - will provide the sprite object involved

        You can specify which mouse button needs to be used for the click using
        the `button` parameter.  It's value needs to be one of "left", "center", 
        "right", "scrollup" or "scrolldown".  The left button is the default.
        '''

        # Convert the button string to a button number
        if isinstance(button, str):
            try:
                button = pgputils.mouse_button_map[button]
            except KeyError:
                raise ValueError("Invalid button!")

        # If a button is valid, add the function to the appropriate button
        if 1 <= button <= 5:
            self._release_funcs[button - 1] = func
        else:
            raise ValueError("Invalid button!")


    def on_drag (self, func, button="left"):
        '''
        Add a function that will be called when the mouse dragged while 
        clicking on this sprite.

        You can provide the following arguments for the function `func`:
         - `x` - will provide x-coordinate of the mouse
         - `y` - will provide y-coordinate of the mouse
         - `pos` - will provide a tuple of the coordinates (x and y) of the mouse
         - `button` - will provide the name of the mouse button used
         - `sprite` - will provide the sprite object involved

        You can specify which mouse button needs to be used for the click using
        the `button` parameter.  It's value needs to be one of "left", "center", 
        "right", "scrollup" or "scrolldown".  The left button is the default.
        '''

        # Convert the button string to a button number
        if isinstance(button, str):
            try:
                button = pgputils.mouse_button_map[button]
            except KeyError:
                raise ValueError("Invalid button!")

        # If a button is valid, add the function to the appropriate button
        if 1 <= button <= 5:
            self._drag_funcs[button - 1] = func
        else:
            raise ValueError("Invalid button!")


        
# What is included when importing *
__all__ = [
    "Sprite"
]
