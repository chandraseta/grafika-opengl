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
    glClearColor(0.3, 0.3, 0.3, 1.0)
    return program

def drawImage(program, images, bg_x_offset, fg_x_offset, fg_y_offset):
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

    for id, image in enumerate(images):
        for i in range(len(image)):
            index_list.append(temp)
            for j in range(1,len(image[i])):
                for k in range(0,3):
                    if id == 0:
                        # Position for Image background
                        if k == 0:
                            vertex_list.append(image[i][j][k] + bg_x_offset)
                        else:
                            vertex_list.append(image[i][j][k])
                    elif id == (len(images)-1):                        
                        # Position for Image foreground
                        if k == 0:
                            vertex_list.append(image[i][j][k] + fg_x_offset)
                        elif k == 1:
                            vertex_list.append(image[i][j][k] + fg_y_offset)
                        else:
                            vertex_list.append(image[i][j][k])
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
        glDrawArrays(GL_POLYGON, index_list[i], index_list[i+1])

    pygame.display.flip()

def draw(images):
    pygame.init()
    pygame.display.set_mode((width, height), HWSURFACE|OPENGL|DOUBLEBUF)

    program = init()

    x_offset = 0
    y_offset = 0

    x_offset_vel = 0
    y_offset_vel = 0

    bg_offset = 0
    bg_offset_vel = 0.0001

    running = True
    while running:
        x_offset += x_offset_vel
        y_offset += y_offset_vel
        bg_offset += bg_offset_vel
        drawImage(program, images, bg_offset, x_offset, y_offset)
        events = pygame.event.get()

        # wait for exit
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    running = False
                if event.key == K_a or event.key == K_LEFT:
                    x_offset_vel -= 0.0005
                if event.key == K_d or event.key == K_RIGHT:
                    x_offset_vel += 0.0005
                if event.key == K_w or event.key == K_UP:
                    y_offset_vel += 0.0001
                if event.key == K_s or event.key == K_DOWN:
                    y_offset_vel -= 0.0001


if __name__ == '__main__':
    print("Hi from car.py")
