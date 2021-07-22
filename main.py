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

ship.set_pen_width(5)
ship.set_fill_color("red")
ship.set_pen_color("white")
ship.pick_pen_up()
# ship.begin_fill()
# ship.set_position(100, 100)
# ship.set_pen_width(10)
# ship.set_position(200, 0)
# ship.set_position(0, 0)
# ship.set_position(10, -100)
# ship.walk_path([(-200, 0), (-100, 100), (0,0)])
# ship.end_fill()

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

# Function that starts and stops drawing
def toggle_drawing ():
    if ship.is_pen_down():
        ship.end_fill()
        ship.pick_pen_up()
    else:
        ship.put_pen_down()
        ship.begin_fill(as_moving=True)

def draw_dot ():
    ship.dot(color="gold")

def draw_stamp ():
    ship.stamp()

# Bind the functions to keys
screen.on_key_hold(on_up, "up")
screen.on_key_hold(on_down, "down")
screen.on_key_hold(on_left, "left")
screen.on_key_hold(on_right, "right")
screen.on_key_hold(esc, "escape")
screen.on_key_press(toggle_drawing, "space")
screen.on_key_press(draw_dot, "d")
screen.on_key_press(draw_stamp, "s")

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
writer = Painter()
writer.hide()
writer.pick_pen_up()
writer.set_position(0, -140)
writer.set_color("gold")


writer.write("Welcome to Space", font="Freedom.ttf", font_size=36)

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
