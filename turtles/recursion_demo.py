import turtle

# Create a turtle object and set the screen's background color to yellow
t = turtle.Turtle()
turtle.getscreen().bgcolor("black")

# Set the turtle's shape, speed, and colors.
# Note: The pen (outline) is set to red and the fill color is set to green.
t.shape("turtle")
t.speed(100)  # Note: Turtle speeds above 10 typically behave as the fastest speed.
t.color("red", "green")

# The following commented code shows a simple star drawing without recursion.
# for i in range(5):
#     anms.forward(50)
#     anms.left(216)

def star(pen, size):
    """
    Recursively draws a star pattern.
    
    :param pen: The turtle object used for drawing.
    :param size: The length of each segment of the star.
    """
    # Base case: stop recursion when the size is too small.
    if size <= 10:
        return
    else:
        # Start filling the shape with the fill color.
        pen.begin_fill()
        for i in range(5):
            pen.forward(size)          # Draw the star's arm.
            star(pen, size/3)          # Recursively draw a smaller star from the current tip.
            pen.left(216)              # Turn left by 216 degrees; equivalent to a right turn of 144 degrees.
        pen.end_fill()
        
# Draw the recursive star with an initial size of 360.
star(t, 360)

# Keep the window open until the user closes it.
turtle.mainloop()
