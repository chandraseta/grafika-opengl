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
    glClearColor(0.9, 0.9, 0.9, 1.0)
    return program

def drawModels(program, models, model_indices, x_offsets, y_offsets, z_offsets):
    # Define Vertice List
    # X Y Z R G B  
    
    # Bind Attribute
    glBindAttribLocation(program, 0, "vPosition")
    glBindAttribLocation(program, 1, "color")

    # Generate Buffers and Bind Buffers
    VBO = glGenBuffers(1)
    VAO = glGenVertexArrays(1)
    EBO = glGenBuffers(1)
    
    index_list = []
    vertex_list = []

    temp = 0
    glBindVertexArray(VAO)

    for id, model in enumerate(models):
        for i in range(len(model)):
            index_list.append(temp)
            for j in range(1,len(model[i])):
                for k in range(0,3):
                    if k == 0:
                        vertex_list.append(model[i][j][k] + x_offsets[id])
                    elif k == 1:
                        vertex_list.append(model[i][j][k] + y_offsets[id])
                    else:
                        vertex_list.append(model[i][j][k] + z_offsets[id])
                for k in range(0,3):
                    # Color
                    vertex_list.append(model[i][0][k])
            index_list.append(j) # Element count
            temp = temp + j

    vertices = numpy.array(vertex_list, numpy.float32)
    indices = numpy.array(model_indices)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices), indices, GL_STATIC_DRAW)

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

def startShowcase(models, indices):
    pygame.init()
    pygame.display.set_mode((width, height), HWSURFACE|OPENGL|DOUBLEBUF)

    program = init()

    x_offsets = []
    y_offsets = []
    z_offsets = []

    x_vels = []
    y_vels = []
    z_vels = []

    # Fill initial value
    for i in range(6):
        x_offsets.append(0)
        y_offsets.append(0)
        z_offsets.append(0)
        x_vels.append(0)
        y_vels.append(0)
        z_vels.append(0)

    running = True
    while running:

        drawModels(program, models, indices, x_offsets, y_offsets, z_offsets)
        events = pygame.event.get()

        # wait for exit
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    running = False

if __name__ == '__main__':
    print("Hi from car.py")
