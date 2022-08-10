---
layout: default
nav_order: 3
---
# Painter

A Painter is a special sub-class of a Sprite with extra methods used to draw on the screen.  All methods of a Sprite object can be used on Painter objects.

Some features of Painter objects include:
 - They can draw on the screen when they move.
 - They can be used to draw filled polygons.
 - They can draw dots and circles.
 - They can stamp copies of their image to the screen.
 - They can write text to the screen.

## Creation

To create a painter sprite, use its constructor.  If no argument is given the painter is invisible.

```python
# Create an invisible painter sprite
my_painter = Painter()
```

If you provide an argument, you are essentially creating a sprite that can also paint.

```python
# Create a painter sprite
my_character = Painter('dog.png')
```

As with a Sprite, you must use add it to the screen for it to appear.

## Drawing and Filling

A painter draws on the screen by putting its pen on the canvas at some starting point and them moving around.  The painter moves around using its [Sprite properties and methods]({{ site.baseurl }}{% link _reference/sprite.md %})

| Property/Method | Description |
| --- | --- |
| `.begin_line()` | Begin drawing a line at the current position.  Movement after this will draw on the screen. |
| `.end_line()` | End drawing a line at the current position.  Movement after this will not draw on the screen. |
| `.drawing` | Whether or not a line is currently being drawn.  Toggling this property has the same effect as calling `.begin_line()` or `.end_line()`.  (default: `False`) |
| `.begin_fill()` | Begin drawing a filled shape at the current position.  This must be followed by a call to `.end_fill()` to finish the filled shape. |
| `.end_fill()` | End drawing a filled shape. |
| `.filling` | Whether or not a filled shape is currently being drawn.  Toggling this property has the same effect as calling `.begin_fill()` or `.end_fill()`.  (default: `False`) |
| `.dot(size, color=None)` | Draw a dot with the given diameter centered at the current location.  You can provide a color or the current line color if not is given. |

## Colors and Sizes

Get or change attributes of the drawings with these properties.

A color can be any of the following:
 - A valid color string.  See https://replit.com/@cjdevet/PygameColors to explore the available color strings.
 - A set of three numbers between 0 and 255 that represent the amount of red, green, blue to use in the color.  A fourth transparency value can be added.
 - An HTML color code in the form "#rrggbb" where each character r, g, b and a are replaced with a hexidecimal digit.  For translucent colors, add another pair of hex digits ("##rrggbbaa").
 - An integer that, when converted to hexidecimal, gives an HTML color code in the form 0xrrggbbaa.
 - A pygame Color object.

| Property/Method | Description |
| --- | --- |
| `.line_color` | The color used to draw lines.  (default: `'black'`) |
| `.fill_color` | The color used for filled shapes.  (default: `'black'`) |
| `.colors` | A 2-tuple with both the line and fill colors.  Setting this to a single color will change both line and fill colors. |
| `.line_width` | The width, in pixels, of lines that are drawn.  (default: `1`) |
| `.step_size` | The step size between points on a line.  Making this value larger can be used to draw dotted lines.  (default: 0.1) |
| `.fill_as_moving` | Whether or not the filled shape will be drawn as the painter moves.  If this is `False`, the filled shape is not drawn until it is finished with `.end_fill()`.  (default: `False`) |

## Shapes

These methods can be used to draw shapes while line drawing is on.

| Property/Method | Description |
| --- | --- |
| `.circle(radius, extent=360)` | Move in a circle with given radius.  The circle will start at the current position and go counterclockwise.  A negative radius will make the circle go clockwise.  Optionally, an arc can be drawn using by making the extent less than 360. |
| `.walk_path(*path, turn=True)` | Move along a path defined by the points given as arguments.  If `turn` is set to `False`, the painter will not change direction as it travels the path. |

## Images and Text

Finally, a painter can stamp images and write text using these methods.

| Property/Method | Description |
| --- | --- |
| `.stamp()` | Stamp a copy of the sprite's image on the screen at the current position. |
| `.write(text, align='middle center', font='Arial', size=12, style=None, color=None)` | Write text on the screen at the current position.  The alignment, font, size, style and color of the text can be specified using keyword arguments.  Use the function's `help()` output for more details. |
