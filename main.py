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
ship.use_smoothing()
ship.scale(0.1)

# The image for a turtle can be rotated.  This function
# sets that the image should rotate whenever the turtle's
# heading changes
ship.set_image_rotates(True)

# Tilt the image so that the ship points in the same direction
# as the heading
ship.set_image_tilt(-90)

ship.set_line_width(5)
ship.set_fill_color("red")
ship.set_line_color("white")

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
    if ship.is_drawing_line():
        ship.end_fill()
        ship.end_line()
    else:
        ship.begin_line()
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
ufo.use_smoothing()
ufo.scale(0.25)
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
screen.add(writer)
writer.set_line_width(5)
writer.set_line_color("gold")
writer.set_fill_color((255, 215, 0, 63))
writer.set_position(-250, -110)
writer.begin_line()
writer.begin_fill()
writer.walk_path([(-250, -170), (250, -170), (250, -110), (-250, -110)])
writer.end_fill()
writer.end_line()
writer.set_position(0, -140)
writer.write("Welcome to Space", font="Freedom.ttf", font_size=36)

def on_drag ():
    ship.set_position(from_pygame_coordinates(pygame.mouse.get_pos()))

ship.on_drag(on_drag)

turtle = Sprite("turtle")
screen.add(turtle)
turtle.set_position(-200, 0)
turtle.set_color("red")
turtle.set_image_rotates()

# Function that moves the turtle forward
def on_w ():
    turtle.move_forward(2)
    wrap_around()

# Function that moves the turtle backward
def on_s ():
    turtle.move_backward(2)
    wrap_around()

# Function that turns the turtle left
def on_a ():
    turtle.turn_left(5)

# Function that turns the turtle right
def on_d ():
    turtle.turn_right(5)

screen.on_key_hold(on_w, "w")
screen.on_key_hold(on_s, "s")
screen.on_key_hold(on_a, "a")
screen.on_key_hold(on_d, "d")

screen.update()

# Start the event loop
start_event_loop(50)
