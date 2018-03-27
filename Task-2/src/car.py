import ctypes
import numpy
import pygame
import time

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from pygame.locals import *  

width = 1024
height = 768

def getFileContents(filename):
    return open(filename, 'r').read()

def init():
    vertexShader = compileShader(getFileContents("data/shaders/triangle.vert"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContents("data/shaders/triangle.frag"), GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)
    
    # Set Clear Color
    glClearColor(0.84705, 0.541176, 0.439215, 1.0)
    return program

def drawImage(program, images, x_offsets, y_offsets):
    # Define Vertice List
    # X Y Z R G B  
    
    # Bind Attribute
    glBindAttribLocation(program, 0, "vPosition")
    glBindAttribLocation(program, 1, "color")

    # Generate Buffers and Bind Buffers
    VBO = glGenBuffers(1)
    VAO = glGenVertexArrays(1)
    
    index_list = []
    vertex_list = []

    temp = 0
    glBindVertexArray(VAO)

    # Background
    index_list.append(temp)
    vertex_list.extend([-1, 0, 0, 0.84705, 0.541176, 0.439215, 
                            -1, 1, 0, 0.91372, 0.89804, 0.80784, 
                            1, 1, 0, 0.91372, 0.89804, 0.80784, 
                            1, 0, 0, 0.84705, 0.541176, 0.439215])
    index_list.append(4)
    temp += 4

    for id, image in enumerate(images):
        for i in range(len(image)):
            index_list.append(temp)
            for j in range(1,len(image[i])):
                for k in range(0,3):
                    # Position for Image foreground
                    if k == 0:
                        vertex_list.append(image[i][j][k] + x_offsets[id])
                    elif k == 1:
                        vertex_list.append(image[i][j][k] + y_offsets[id])
                    else:
                        vertex_list.append(image[i][j][k])
                for k in range(0,3):
                    # Color
                    vertex_list.append(image[i][0][k])   
            index_list.append(j) #element count
            temp = temp + j

    vertices = numpy.array(vertex_list, numpy.float32)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW) # Copy data to buffer

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_TRUE, 24, ctypes.c_void_p(0))
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    # Draw and Run
    glViewport(0, 0, width, height)
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)

    glBindVertexArray(VAO)
    for i in range(0,len(index_list),2):
        glDrawArrays(GL_POLYGON, index_list[i], index_list[i+1] )

    pygame.display.flip()

def draw(images):
    pygame.init()
    pygame.display.set_mode((width, height), HWSURFACE|OPENGL|DOUBLEBUF)

    program = init()

    x_offsets = []
    y_offsets = []

    x_vels = []
    y_vels = []

    # Fill initial value
    for i in range(6):
        x_offsets.append(0)
        y_offsets.append(0)
        x_vels.append(0)
        y_vels.append(0)

    x_offsets[0] = -1
    x_offsets[1] = -0.6
    x_offsets[2] = -0.5
    x_offsets[3] = -4
    y_offsets[5] = -0.6

    x_vels[0] = 0.000075
    x_vels[1] = 0.000025
    x_vels[2] = 0.0008
    x_vels[3] = 0.002
    x_vels[4] = 0.008

    running = True
    while running:
        for i in range(6):
            x_offsets[i] += x_vels[i]
            y_offsets[i] += y_vels[i]
            if i == 0:
                # Cloud
                if x_offsets[i] > 3:
                    x_offsets[i] = -2.7
            # elif i == 1:
            #     # Mountain

            if i == 2:
                # Building - Back
                if x_offsets[i] > 2:
                    x_offsets[i] = -0.8
            elif i == 3:
                # Building - Front
                if x_offsets[i] > 0.8:
                    x_offsets[i] = -3
            elif i == 4:
                # Road
                if x_offsets[i] > 0.8:
                    x_offsets[i] = -0.2
            elif i == 5:
                # Regalia
                if y_offsets[i] > -0.6:
                    y_offsets[i] = -0.6
                    y_vels[i] = 0
                if y_offsets[i] < -0.9:
                    y_offsets[i] = -0.9
                    y_vels[i] = 0

        drawImage(program, images, x_offsets, y_offsets)
        events = pygame.event.get()

        # wait for exit
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    running = False
                if event.key == K_a or event.key == K_LEFT:
                    x_vels[5] -= 0.0002
                if event.key == K_d or event.key == K_RIGHT:
                    x_vels[5] += 0.0002
                if event.key == K_w or event.key == K_UP:
                    y_vels[5] += 0.0001
                if event.key == K_s or event.key == K_DOWN:
                    y_vels[5] -= 0.0001


if __name__ == '__main__':
    print("Hi from car.py")
