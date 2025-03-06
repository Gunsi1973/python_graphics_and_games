import pygame
import math
import random
import colorsys

# Initialize PyGame
pygame.init()

# Window size and colors
width, height = 1000, 1000  # You can try different sizes
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animated Lissajous Figure: Frequencies and Color")

# Layout calculations:
drawing_area_height = int(height * 0.8)       # Drawing area occupies 80% of the window height
control_area_height = height - drawing_area_height  # Control area occupies the bottom 20%
slider_area_y = drawing_area_height           # Top of the control area

slider_row_gap = int(0.05 * control_area_height)
slider_margin_x = int(0.05 * width)
slider_width = int(0.4 * width)
slider_height = 20

# Frequency sliders row (for X and Y frequencies)
freq_slider_y = slider_area_y + slider_row_gap

# Button row 1 (Reset and Randomize)
button_width = int(0.12 * width)
button_height = 30
button_row1_y = freq_slider_y + slider_height + slider_row_gap
gap = int(0.05 * width)
row1_total_width = 2 * button_width + gap
start_x_row1 = (width - row1_total_width) // 2
reset_button_x = start_x_row1
random_button_x = start_x_row1 + button_width + gap

# Button row 2 (Color Cycle, Gradient, Reset Mode)
button_row2_y = button_row1_y + button_height + slider_row_gap
row2_total_width = 3 * button_width + 2 * gap
start_x_row2 = (width - row2_total_width) // 2
color_cycle_button_x = start_x_row2
gradient_button_x = start_x_row2 + button_width + gap
reset_mode_button_x = start_x_row2 + 2 * (button_width + gap)

# Helper functions for color conversion and gradient calculation
def hsv_to_rgb(h):
    """Convert a hue value (0-1) with full saturation and brightness to an RGB tuple."""
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, 1, 1)
    return (int(r * 255), int(g * 255), int(b * 255))

def get_gradient_color(x, y):
    """Compute a gradient color based on the dot's position."""
    r = int(x / width * 255)
    g = int(y / drawing_area_height * 255)
    b = int(((x / width) + (y / drawing_area_height)) / 2 * 255)
    return (r, g, b)

# Global drawing mode: 0 = white, 1 = color cycle, 2 = gradient
drawing_mode = 0
hue = 0  # global hue for color cycle

# Slider class
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.label = label
        self.handle_radius = h // 4  # 50% of previous size
        self.handle_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.w
        self.dragging = False

    def draw(self, screen, font):
        # Draw the slider line as a red bar 2 pixels high
        line_y = self.y + self.h // 2 - 1
        pygame.draw.rect(screen, (255, 0, 0), (self.x, line_y, self.w, 2))
        # Draw the handle as a yellow circle
        pygame.draw.circle(screen, (255, 255, 0), (int(self.handle_x), self.y + self.h // 2), self.handle_radius)
        # Draw the label and current value
        text = font.render(f"{self.label}: {self.value:.2f}", True, white)
        screen.blit(text, (self.x, self.y - 25))

    def update(self, mouse_x):
        self.handle_x = max(self.x, min(mouse_x, self.x + self.w))
        ratio = (self.handle_x - self.x) / self.w
        self.value = self.min_val + ratio * (self.max_val - self.min_val)

    def update_handle(self):
        self.handle_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.w

# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, (180, 180, 180), self.rect)
        text_surf = font.render(self.text, True, black)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Font for labels and buttons
font = pygame.font.SysFont(None, 24)

# Frequency sliders with starting values: X = 2.7, Y = 3.3; range [0.1, 9]
slider_freq_x = Slider(slider_margin_x, freq_slider_y, slider_width, slider_height, 0.1, 9, 2.7, "Frequency X")
slider_freq_y = Slider(slider_margin_x * 2 + slider_width, freq_slider_y, slider_width, slider_height, 0.1, 9, 3.3, "Frequency Y")
sliders = [slider_freq_x, slider_freq_y]

# Instantiate buttons
reset_button = Button(reset_button_x, button_row1_y, button_width, button_height, "Reset")
random_button = Button(random_button_x, button_row1_y, button_width, button_height, "Randomize")
color_cycle_button = Button(color_cycle_button_x, button_row2_y, button_width, button_height, "Color Cycle")
gradient_button = Button(gradient_button_x, button_row2_y, button_width, button_height, "Gradient")
reset_mode_button = Button(reset_mode_button_x, button_row2_y, button_width, button_height, "Reset Mode")

# Fixed amplitudes (as in the original code)
amplitude_x = width // 3
amplitude_y = drawing_area_height // 3

# Constant phase shift (set to 2)
phase_shift = 2

# Time variable and clock
t = 0
clock = pygame.time.Clock()

# Create a surface as a canvas for the Lissajous points
canvas = pygame.Surface((width, drawing_area_height))
canvas.fill(black)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if any slider is clicked
            for slider in sliders:
                if slider.x <= mouse_pos[0] <= slider.x + slider.w and slider.y <= mouse_pos[1] <= slider.y + slider.h:
                    slider.dragging = True
            # Button actions
            if reset_button.is_clicked(mouse_pos):
                canvas.fill(black)
            if random_button.is_clicked(mouse_pos):
                slider_freq_x.value = random.uniform(slider_freq_x.min_val, slider_freq_x.max_val)
                slider_freq_y.value = random.uniform(slider_freq_y.min_val, slider_freq_y.max_val)
                slider_freq_x.update_handle()
                slider_freq_y.update_handle()
                canvas.fill(black)
            if color_cycle_button.is_clicked(mouse_pos):
                drawing_mode = 1
                hue = 0
                canvas.fill(black)
            if gradient_button.is_clicked(mouse_pos):
                drawing_mode = 2
                canvas.fill(black)
            if reset_mode_button.is_clicked(mouse_pos):
                drawing_mode = 0
                canvas.fill(black)

        elif event.type == pygame.MOUSEBUTTONUP:
            for slider in sliders:
                slider.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, _ = event.pos
            for slider in sliders:
                if slider.dragging:
                    slider.update(mouse_x)

    # Get frequency parameters from sliders
    freq_x = slider_freq_x.value
    freq_y = slider_freq_y.value

    # Compute new coordinates for the Lissajous figure
    x = int(width / 2 + amplitude_x * math.sin(freq_x * t + phase_shift))
    y = int(drawing_area_height / 2 + amplitude_y * math.cos(freq_y * t))
    
    # Determine the dot color based on the drawing mode
    if drawing_mode == 0:
        dot_color = white
    elif drawing_mode == 1:
        dot_color = hsv_to_rgb(hue)
        hue += 0.001  # slower hue cycle
    elif drawing_mode == 2:
        dot_color = get_gradient_color(x, y)
    
    # Draw the point on the canvas (smaller dots: radius 1)
    pygame.draw.circle(canvas, dot_color, (x, y), 1)
    
    # Increase the time variable
    t += 0.02
    
    # Blit the canvas onto the upper area of the screen
    screen.blit(canvas, (0, 0))
    
    # Redraw the control area (bottom)
    pygame.draw.rect(screen, black, (0, slider_area_y, width, control_area_height))
    for slider in sliders:
        slider.draw(screen, font)
    reset_button.draw(screen, font)
    random_button.draw(screen, font)
    color_cycle_button.draw(screen, font)
    gradient_button.draw(screen, font)
    reset_mode_button.draw(screen, font)
    
    pygame.display.flip()
    clock.tick(120)

pygame.quit()
