from turtle import *

# Set the drawing (ink) color to red.
color("red")

# Begin the filling process to fill the heart shape with red.
begin_fill()

# Set the pen width to 4 pixels.
pensize(4)

# Rotate left by 50° to start drawing the left side of the heart.
left(50)

# Draw the first straight line (one side of the heart).
forward(133)

# Draw the first arc of the heart with a radius of 50 and an arc of 200°.
circle(50, 200)

# Adjust the heading by turning right 140°.
right(140)

# Draw the second arc of the heart.
circle(50, 200)

# Draw the second straight line, completing the heart shape.
forward(133)

# End the filling process to fill the drawn shape with red.
end_fill()

# Keep the window open until it is closed manually.
done()
