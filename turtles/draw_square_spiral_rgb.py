import turtle

def draw_color_spiral():
    """
    Draws a spiral that changes pen color gradually.
    
    The spiral increases in length on each iteration and rotates by 91°,
    while the pen color cycles through a range of colors.
    """
    # Create a turtle object and screen, then set up the screen.
    t = turtle.Turtle()
    screen = turtle.Screen()
    screen.bgcolor('black')
    
    # Set the color mode to 255 to allow RGB values between 0-255.
    turtle.colormode(255)
    
    # Set drawing speed.
    t.speed(15)
    
    # Initialize color values: starting with red.
    r, g, b = 255, 0, 0
    
    # Draw a spiral with 510 iterations.
    for i in range(255 * 2):
        # Adjust color based on the current iteration.
        if i < 255 // 3:
            g += 3
        elif i < (255 * 2) // 3:
            r -= 3
        elif i < 255:
            b += 3
        elif i < (255 * 4) // 3:
            g -= 3
        elif i < (255 * 5) // 3:
            r += 3
        else:
            b -= 3
        
        # Draw the spiral pattern: move forward with increasing length and turn.
        t.forward(50 + i)
        t.right(91)
        t.pencolor(r, g, b)
    
    # Keep the window open until manually closed.
    screen.mainloop()

def main():
    draw_color_spiral()

if __name__ == '__main__':
    main()
