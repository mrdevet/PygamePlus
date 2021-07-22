# Programmer: Mr. Devet
# Date: June 11, 2021
# Purpose: Illustrate new features of the superturtle module

from screen import *
from sprite import *
from painter import *
from event_loop import *
import pygame

pygame.init()

# Set up the screen
screen = Screen(640, 360, "PyGame Plus")
screen.open()

# We can use image files that are not GIFs
screen.set_background_image("space.jpg")

# Create a "ship" turtle
ship = Painter("ship.png")
screen.add(ship)

# We can scale the image of a turtle.  In this example, 
# the ship's image is scaled by a factor of 0.1 (or 10%)
ship.scale(0.1, smooth=True)

# The image for a turtle can be rotated.  This function
# sets that the image should rotate whenever the turtle's
# heading changes
ship.set_image_rotates(True)

# Tilt the image so that the ship points in the same direction
# as the heading
ship.set_image_tilt(-90)

ship.set_fill_color("red")
ship.set_pen_color("white")
ship.begin_fill()
ship.set_position(100, 100)
ship.set_pen_width(10)
ship.set_position(200, 0)
ship.set_position(0, 0)
ship.set_position(10, -100)

ship.walk_path([(-200, 0), (-100, 100), (0,0)])
ship.end_fill()

# Function that ends the program
def esc ():
    end_event_loop()

# Function that checks if the ship is off the screen and
# moves it to the other side
def wrap_around ():
    if ship.get_x() >= 345:
        ship.set_x(-345)
    elif ship.get_x() <= -345:
        ship.set_x(345)
    if ship.get_y() >= 205:
        ship.set_y(-205)
    elif ship.get_y() <= -205:
        ship.set_y(205)

# Function that moves the ship forward
def on_up ():
    ship.move_forward(2)
    wrap_around()

# Function that moves the ship backward
def on_down ():
    ship.move_backward(2)
    wrap_around()

# Function that turns the ship left
def on_left ():
    ship.turn_left(5)

# Function that turns the ship right
def on_right ():
    ship.turn_right(5)

# Bind the functions to keys
screen.on_key_hold(on_up, "up")
screen.on_key_hold(on_down, "down")
screen.on_key_hold(on_left, "left")
screen.on_key_hold(on_right, "right")
screen.on_key_hold(esc, "escape")

# Create a "ufo" turtle
ufo = Sprite("ufo.png")
screen.add(ufo)
ufo.scale(0.25, smooth=True)
ufo.set_position(0, 100)

# Function that moves the ufo forward
def move_ufo ():
    ufo.move_forward(1)
    if ufo.get_x() >= 332:
        ufo.set_x(-332)
    if ship.is_touching(ufo, method="mask"):
        ship.set_position(0, 0)

ufo.on_update(move_ufo)

# # Create a turtle to write text to the screen
# writer = turtle.Turtle()
# writer.hideturtle()
# writer.penup()
# writer.goto(0, -160)
# writer.color("gold")

# # FEATURE: The .write() method has had some features added:
# #  - `align` is where the turtle writing aligns with the text.
# #    It is a string containing "left", "right", "center", "top",
# #    "bottom", "middle" or a combination separated by space
# #    (e.g. "bottom center")
# #  - `font` can be the name of a font on the system or a
# #    True Type Font file (.ttf)
# #  - `font_size` is the height of the text in pixels
# #  - `font_style` can be "bold", "italic", "underline" or a 
# #    combination separated by space (e.g. "bold italic")
# writer.write("Welcome to Space", align="center", 
#              font="Freedom.ttf", font_size=36)

def on_click ():
    print("CLICKED")

def on_release ():
    print("RELEASED")

def on_drag ():
    ship.set_position(from_pygame_coordinates(pygame.mouse.get_pos()))

ship.on_click(on_click)
ship.on_release(on_release)
ship.on_drag(on_drag)

screen.update()

# Start the event loop
start_event_loop(50)
