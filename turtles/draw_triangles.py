import turtle

def draw_pattern(t):
    """
    Draw a colorful spiral pattern using the given turtle object.
    
    The turtle draws lines of increasing length while rotating by 121° each iteration,
    using a cycle of three colors for a dynamic visual effect.
    """
    # Define the tuple of colors to cycle through.
    colors = ('white', 'pink', 'cyan')
    
    # Set the pen width and speed.
    t.width(2)
    t.speed(15)
    
    # Draw 300 line segments, changing color and angle each time.
    for i in range(300):
        t.pencolor(colors[i % len(colors)])
        t.forward(i * 4)
        t.right(121)

def main():
    # Set up the screen with a black background.
    screen = turtle.Screen()
    screen.bgcolor("black")
    
    # Create a turtle object.
    t = turtle.Turtle()
    
    # Draw the pattern.
    draw_pattern(t)
    
    # Keep the window open until it is closed manually.
    screen.mainloop()

if __name__ == '__main__':
    main()
