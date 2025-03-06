import pygame
import math
import numpy as np

pygame.init()

# -------------------
# Window & Layout Setup
# -------------------
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Lissajous Sculpture (Closed Loop)")

# Define drawing and control areas
drawing_area_height = int(height * 0.8)
control_area_height = height - drawing_area_height

# -------------------
# Slider Class Definition
# -------------------
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial  # We'll round this value when using it.
        self.label = label
        self.handle_radius = h // 4
        self.handle_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.w
        self.dragging = False

    def draw(self, screen, font):
        line_y = self.y + self.h // 2 - 1
        pygame.draw.rect(screen, (255, 0, 0), (self.x, line_y, self.w, 2))
        pygame.draw.circle(screen, (255, 255, 0), (int(self.handle_x), self.y + self.h // 2), self.handle_radius)
        text = font.render(f"{self.label}: {self.value:.2f}", True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 25))

    def update(self, mouse_x):
        self.handle_x = max(self.x, min(mouse_x, self.x + self.w))
        ratio = (self.handle_x - self.x) / self.w
        self.value = self.min_val + ratio * (self.max_val - self.min_val)

    def update_handle(self):
        self.handle_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.w

# -------------------
# Projection and Rotation Functions
# -------------------
center_x, center_y = width // 2, drawing_area_height // 2
d = 500  # projection distance

def project(x, y, z):
    factor = d / (z + d)
    proj_x = center_x + x * factor
    proj_y = center_y - y * factor
    return int(proj_x), int(proj_y)

def rotateY(x, y, z, angle):
    cosA = math.cos(angle)
    sinA = math.sin(angle)
    x_new = x * cosA + z * sinA
    z_new = -x * sinA + z * cosA
    return x_new, y, z_new

def rotateX(x, y, z, angle):
    cosA = math.cos(angle)
    sinA = math.sin(angle)
    y_new = y * cosA - z * sinA
    z_new = y * sinA + z * cosA
    return x, y_new, z_new

# -------------------
# 3D Lissajous Parameters
# -------------------
A, B, C = 200, 200, 200  # Amplitudes
# Fixed phase shifts
delta_x, delta_y, delta_z = 0, math.pi/2, math.pi/4

# -------------------
# Interactive Rotation Variables
# -------------------
rot_x = 0.0
rot_y = 0.0
vel_x = 0.0
vel_y = 0.0
dragging_sculpture = False
mouse_last_x, mouse_last_y = 0, 0

# -------------------
# Slider Setup (One Slider in the Control Area)
# -------------------
font = pygame.font.SysFont(None, 24)
slider_height = 20
# We'll center the slider horizontally.
slider_width = int(width * 0.5)
left_margin = (width - slider_width) // 2
slider_y = drawing_area_height + (control_area_height - slider_height) // 2

# Slider range is from 1 to 9. The slider value is rounded to integer.
base_freq_slider = Slider(left_margin, slider_y, slider_width, slider_height, 1, 9, 3, "Base Frequency")

# -------------------
# Animation Variables
# -------------------
t_offset = 0.0
num_points = 800
dt = 0.01

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Distinguish clicks in drawing area vs. control area
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < drawing_area_height:
                dragging_sculpture = True
                mouse_last_x, mouse_last_y = event.pos
            else:
                if base_freq_slider.x <= event.pos[0] <= base_freq_slider.x + base_freq_slider.w and \
                   base_freq_slider.y <= event.pos[1] <= base_freq_slider.y + base_freq_slider.h:
                    base_freq_slider.dragging = True

        if event.type == pygame.MOUSEMOTION:
            if dragging_sculpture:
                dx = event.pos[0] - mouse_last_x
                dy = event.pos[1] - mouse_last_y
                sensitivity = 0.005
                rot_y += dx * sensitivity
                rot_x += dy * sensitivity
                vel_y = dx * sensitivity
                vel_x = dy * sensitivity
                mouse_last_x, mouse_last_y = event.pos
            else:
                if base_freq_slider.dragging:
                    base_freq_slider.update(event.pos[0])
                    
        if event.type == pygame.MOUSEBUTTONUP:
            dragging_sculpture = False
            base_freq_slider.dragging = False

    # Apply momentum when not dragging
    if not dragging_sculpture:
        rot_x += vel_x
        rot_y += vel_y
        friction = 0.99
        vel_x *= friction
        vel_y *= friction

    # Use the slider value (rounded) as the base frequency
    base_freq = int(round(base_freq_slider.value))
    freq_x = base_freq
    freq_y = base_freq + 1
    freq_z = base_freq + 2

    # -------------------
    # Compute 3D Lissajous Points with Interactive Rotation
    # -------------------
    points = []
    for i in range(num_points):
        t = t_offset + i * dt
        x = A * math.sin(freq_x * t + delta_x)
        y = B * math.sin(freq_y * t + delta_y)
        z = C * math.sin(freq_z * t + delta_z)
        # Apply rotations
        x, y, z = rotateY(x, y, z, rot_y)
        x, y, z = rotateX(x, y, z, rot_x)
        p = project(x, y, z)
        points.append(p)

    # -------------------
    # Drawing
    # -------------------
    screen.fill((0, 0, 0))
    if len(points) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
    # Draw red ball along the curve
    ball_index = int((t_offset * 100) % num_points)
    pygame.draw.circle(screen, (255, 0, 0), points[ball_index], 8)
    # Draw control area background and slider
    pygame.draw.rect(screen, (30, 30, 30), (0, drawing_area_height, width, control_area_height))
    base_freq_slider.draw(screen, font)

    pygame.display.flip()
    clock.tick(60)
    t_offset += 0.01

pygame.quit()
