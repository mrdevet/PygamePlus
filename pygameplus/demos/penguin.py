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

from importlib import resources
from pygameplus import *

# Set up the screen
screen = Screen(640, 360, "PyGame Plus Penguin")

# Lists to hold the background sprites
left_backgrounds = []
right_backgrounds = []

# Dictionary to hold the penguin images
penguin_images = {}

# The penguin sprite (it currently doesn't have a picture)
penguin = Sprite()

# Function that ends the program
def quit ():
    stop_event_loop()

screen.on_key_press(quit, "escape")

# Function to start the program
def main ():
    # Open the screen
    screen.open()

    # Load the background images
    for i in range(1, 9):
        with resources.path("pygameplus.demos.img", f"snow{i}.png") as image_path:
            picture = load_picture(image_path)

        left_background = Sprite(picture)
        left_background.scale_factor = 1 / 3
        left_backgrounds.append(left_background)
        screen.add(left_background)

        right_background = Sprite(picture)
        right_background.scale_factor = 1 / 3
        right_background.x = 640
        right_backgrounds.append(right_background)
        screen.add(right_background)

    # Load the penguin images
    penguin_states = ["stand", "walk0", "walk1", "walk2", "walk3", "slide",
                      "jump0", "jump1", "jump2"]
    for state in penguin_states:
        with resources.path("pygameplus.demos.img", f"penguin_{state}.png") as image_path:
            penguin_images[state] = load_picture(image_path)

    # Set the penguins initial picture
    penguin.picture = penguin_images["stand"]

    # Config the penguin
    penguin.y = -100
    penguin.scale_factor = 0.5
    screen.add(penguin)

    screen.update()

    # Start the event loop
    start_event_loop(50)


# call the "main" function if running this script
if __name__ == "__main__":
    main()
