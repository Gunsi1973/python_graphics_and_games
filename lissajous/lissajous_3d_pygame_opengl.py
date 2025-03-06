# Install OpenGL with
# pip install PyOpenGL PyOpenGL_accelerate
# 

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Window dimensions
width, height = 1000, 800

def init_gl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glPointSize(8.0)

def draw_lissajous(t_offset):
    # 3D Lissajous parameters
    A, B, C = 200, 200, 200  # Amplitudes
    freq_x, freq_y, freq_z = 3, 4, 5  # Frequencies (integers -> closed loop)
    delta_x, delta_y, delta_z = 0, math.pi/2, math.pi/4  # Phase shifts

    num_points = 800
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_STRIP)
    for i in range(num_points):
        t = t_offset + i * 0.01
        x = A * math.sin(freq_x * t + delta_x)
        y = B * math.sin(freq_y * t + delta_y)
        z = C * math.sin(freq_z * t + delta_z)
        glVertex3f(x, y, z)
    glEnd()

    # Compute red ball position along the curve
    ball_index = int((t_offset * 100) % num_points)
    t = t_offset + ball_index * 0.01
    x = A * math.sin(freq_x * t + delta_x)
    y = B * math.sin(freq_y * t + delta_y)
    z = C * math.sin(freq_z * t + delta_z)
    
    # Draw red sphere at the computed position
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluSphere(quadric, 8, 16, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def main():
    pygame.init()
    display = (width, height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Lissajous Sculpture (PyOpenGL with Zoom)")
    
    # Set up perspective once (we'll reload each frame)
    gluPerspective(45, (display[0] / display[1]), 0.1, 2000.0)

    init_gl()
    
    clock = pygame.time.Clock()
    t_offset = 0.0

    # Variables for interactive rotation
    rot_x, rot_y = 0.0, 0.0
    vel_x, vel_y = 0.0, 0.0
    dragging = False
    last_mouse_x, last_mouse_y = 0, 0
    
    # Zoom variable controls camera distance (initially -600)
    zoom = -600.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click starts dragging
                    dragging = True
                    last_mouse_x, last_mouse_y = event.pos
                elif event.button == 4:  # Scroll up: zoom in
                    zoom += 20
                elif event.button == 5:  # Scroll down: zoom out
                    zoom -= 20

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == MOUSEMOTION:
                if dragging:
                    dx = event.pos[0] - last_mouse_x
                    dy = event.pos[1] - last_mouse_y
                    sensitivity = 0.5  # adjust sensitivity as needed
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

        # Each frame, reset the modelview matrix to apply zoom and rotation
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Reload perspective projection
        gluPerspective(45, (display[0] / display[1]), 0.1, 2000.0)
        # Apply zoom translation
        glTranslatef(0.0, 0.0, zoom)

        glPushMatrix()
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)
        draw_lissajous(t_offset)
        glPopMatrix()
        
        pygame.display.flip()
        clock.tick(60)
        t_offset += 0.005

    pygame.quit()

if __name__ == "__main__":
    main()
