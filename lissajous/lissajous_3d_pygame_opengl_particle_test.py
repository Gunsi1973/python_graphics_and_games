import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# ---------------------------
# OpenGL & Pygame Setup
# ---------------------------
width, height = 1000, 800
pygame.init()
display = (width, height)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Lissajous Sculpture with Burning Particle Effects")

# Enable blending for particles (smooth alpha fade)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

gluPerspective(45, (display[0] / display[1]), 0.1, 2000.0)
glTranslatef(0.0, 0.0, -600)
glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)

clock = pygame.time.Clock()

# ---------------------------
# Global Variables for Interactive Rotation
# ---------------------------
rot_x, rot_y = 0.0, 0.0
vel_x, vel_y = 0.0, 0.0
dragging = False
last_mouse_x, last_mouse_y = 0, 0

# ---------------------------
# Lissajous Parameters (Closed Loop)
# ---------------------------
A, B, C = 200, 200, 200      # Amplitudes
freq_x, freq_y, freq_z = 3, 4, 5  # Frequencies (integers => closed loop)
delta_x, delta_y, delta_z = 0, math.pi/2, math.pi/4  # Phase shifts

# ---------------------------
# Animation Parameter
# ---------------------------
t_offset = 0.0
dt = 0.01
num_points = 800

# ---------------------------
# Particle System Setup
# ---------------------------
# Each particle is a dict with position, velocity, age, and lifetime.
particles = []  
particle_spawn_rate = 5  # spawn 5 particles per frame
particle_lifetime = 1.5  # seconds

def update_particles(dt):
    global particles
    # Update each particle
    new_particles = []
    for p in particles:
        p['age'] += dt
        if p['age'] < p['lifetime']:
            # Update position
            p['pos'][0] += p['vel'][0] * dt
            p['pos'][1] += p['vel'][1] * dt
            p['pos'][2] += p['vel'][2] * dt
            new_particles.append(p)
    particles = new_particles

def draw_particles():
    glPointSize(6.0)
    glBegin(GL_POINTS)
    for p in particles:
        # Compute alpha (fades from 1 to 0 over lifetime)
        alpha = max(0.0, 1 - (p['age'] / p['lifetime']))
        # We'll use an orange color for embers.
        glColor4f(1.0, 0.5, 0.0, alpha)
        glVertex3f(p['pos'][0], p['pos'][1], p['pos'][2])
    glEnd()

def spawn_particles(emitter_pos):
    # Spawn a few particles at the emitter (red ball) position with small random velocities.
    for _ in range(particle_spawn_rate):
        particle = {
            'pos': [emitter_pos[0], emitter_pos[1], emitter_pos[2]],
            'vel': [random.uniform(-20, 20), random.uniform(10, 40), random.uniform(-20, 20)],
            'age': 0.0,
            'lifetime': particle_lifetime
        }
        particles.append(particle)

# ---------------------------
# Utility: 3D Rotation Functions
# ---------------------------
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

# ---------------------------
# Utility: Compute Red Ball Position on Lissajous Curve
# ---------------------------
def get_red_ball_position(t_offset, rot_x, rot_y):
    # Compute red ball position using same parameters as the curve.
    ball_index = int((t_offset * 100) % num_points)
    t = t_offset + ball_index * 0.01
    x = A * math.sin(freq_x * t + delta_x)
    y = B * math.sin(freq_y * t + delta_y)
    z = C * math.sin(freq_z * t + delta_z)
    # Apply interactive rotations
    x, y, z = rotateY(x, y, z, rot_y)
    x, y, z = rotateX(x, y, z, rot_x)
    return (x, y, z)

# ---------------------------
# Draw the 3D Lissajous Curve and Red Ball
# ---------------------------
def draw_lissajous(t_offset, rot_x, rot_y):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_STRIP)
    for i in range(num_points):
        t = t_offset + i * dt
        x = A * math.sin(freq_x * t + delta_x)
        y = B * math.sin(freq_y * t + delta_y)
        z = C * math.sin(freq_z * t + delta_z)
        # Apply rotation
        x, y, z = rotateY(x, y, z, rot_y)
        x, y, z = rotateX(x, y, z, rot_x)
        glVertex3f(x, y, z)
    glEnd()
    
    # Draw red ball
    ball_pos = get_red_ball_position(t_offset, rot_x, rot_y)
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(ball_pos[0], ball_pos[1], ball_pos[2])
    quadric = gluNewQuadric()
    gluSphere(quadric, 8, 16, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    
    return ball_pos

# ---------------------------
# Main Loop
# ---------------------------
running = True
while running:
    dt_sec = clock.tick(60) / 1000.0  # seconds elapsed since last frame
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                dragging = True
                last_mouse_x, last_mouse_y = event.pos

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        elif event.type == MOUSEMOTION:
            if dragging:
                dx = event.pos[0] - last_mouse_x
                dy = event.pos[1] - last_mouse_y
                sensitivity = 0.5
                rot_y += dx * sensitivity
                rot_x += dy * sensitivity
                vel_y = dx * sensitivity
                vel_x = dy * sensitivity
                last_mouse_x, last_mouse_y = event.pos

    if not dragging:
        rot_x += vel_x
        rot_y += vel_y
        friction = 0.99
        vel_x *= friction
        vel_y *= friction

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # Maintain camera setup
    gluPerspective(45, (display[0] / display[1]), 0.1, 2000.0)
    glTranslatef(0.0, 0.0, -600)

    glPushMatrix()
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    
    # Draw the Lissajous curve and red ball; get red ball position
    red_ball_pos = draw_lissajous(t_offset, rot_x, rot_y)
    
    # Spawn particles at the red ball position
    spawn_particles(red_ball_pos)
    # Update and draw particles
    update_particles(dt_sec)
    draw_particles()
    
    glPopMatrix()
    
    pygame.display.flip()
    t_offset += 0.005

pygame.quit()
