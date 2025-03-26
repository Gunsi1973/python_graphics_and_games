import turtle
import colorsys

def draw_color_spiral():
    t = turtle.Turtle()
    screen = turtle.Screen()
    screen.bgcolor('black')
    turtle.colormode(255)
    t.speed(15)
    t.width(2)
    
    total_iterations = 255 * 2  # 510 iterations total
    for i in range(total_iterations):
        # Map i to a hue value between 0 and 1.
        hue = i / total_iterations
        # Convert the HSV color (with full saturation and value) to RGB.
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        # Scale the values to 0-255.
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        
        t.pencolor(r, g, b)
        t.forward(50 + i)
        t.right(91)
    
    screen.mainloop()

def main():
    draw_color_spiral()

if __name__ == '__main__':
    main()
