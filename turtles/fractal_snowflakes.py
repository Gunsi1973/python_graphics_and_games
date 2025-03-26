import turtle  # Import the turtle graphics module

# Set up the screen with a black background.
screen = turtle.Screen()
screen.bgcolor("black")

def snowflake(t, lengthSide, levels):
    """
    Recursively draws one side of a Koch snowflake.
    
    Parameters:
      t         -- the turtle object used for drawing
      lengthSide -- the length of the current segment
      levels    -- the recursion depth; when 0, a straight line is drawn
    """
    if levels == 0:
        t.forward(lengthSide)  # Draw a straight line when recursion ends
        return
    # Divide the current segment into thirds for the Koch curve.
    lengthSide /= 3.0

    snowflake(t, lengthSide, levels - 1)  # Draw first segment
    t.left(60)                          # Turn to create the spike
    snowflake(t, lengthSide, levels - 1)  # Draw second segment
    t.right(120)                        # Turn to create the opposite spike
    snowflake(t, lengthSide, levels - 1)  # Draw third segment
    t.left(60)                          # Reorient for the final segment
    snowflake(t, lengthSide, levels - 1)  # Draw fourth segment

# Create a turtle object named 't'
t = turtle.Turtle()

# Set the drawing (ink) color to red.
t.color("red")

# Set the drawing speed to the fastest setting (0 for instant drawing).
t.speed(0)

length = 300.0  # Define the side length for the snowflake

# Reposition the turtle to better center the drawing.
t.penup()
t.fd(-150)
t.pendown()

# Draw a Koch snowflake by drawing three snowflake sides.
for i in range(3):
    snowflake(t, length, 4)  # Draw one side with 4 recursion levels
    t.right(120)            # Turn 120° for the next side

turtle.mainloop()  # Keep the window open until the user closes it.
