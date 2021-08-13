# Programmer: Mr. Devet
# Date: June 11, 2021
# Purpose: Illustrate new features of the superturtle module

from screen import Screen
from turtle import *
import pygame

pygame.init()

# Set up the screen
screen = Screen(640, 360, "PyGame Plus")
screen.open()

# Create a turtle
michaelangelo = Turtle()
screen.add(michaelangelo)

michaelangelo.begin_line()
michaelangelo.set_line_color("blue")
michaelangelo.set_line_width(5)

michaelangelo.move_forward(99)
michaelangelo.turn_left(90)

michaelangelo.set_speed(480)
michaelangelo.move_forward(99)
michaelangelo.turn_left(90)

michaelangelo.set_speed(60)
michaelangelo.disable_animations()
michaelangelo.move_forward(99)
michaelangelo.turn_left(90)
michaelangelo.move_forward(99)
michaelangelo.turn_left(180)

michaelangelo.enable_animations()

michaelangelo.set_fill_color("red")
michaelangelo.begin_fill()
michaelangelo.circle(50)
michaelangelo.end_fill()
