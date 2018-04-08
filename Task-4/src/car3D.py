import ctypes
import math
import numpy
import pygame
import time
import transformations

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from pygame.locals import *  

DEGREE = math.pi / 180

width = 800
height = 600

def getFileContents(filename):
    return open(filename, 'r').read()

def init():
    pygame.init()
    
    vertexShader = compileShader(getFileContents("data/shaders/triangle.vert"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContents("data/shaders/triangle.frag"), GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)
    
    # Set Clear Color
    glClearColor(0.9, 0.9, 0.9, 1.0)
    return program

def drawModels(program, models, model_indices, x_offsets, y_offsets, z_offsets, transform):
    # Define Vertice List
    # X Y Z R G B  
    
    # Bind Attribute
    glBindAttribLocation(program, 0, "vPosition")
    glBindAttribLocation(program, 1, "color")

    # Generate Buffers and Bind Buffers
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    
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

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_TRUE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    # EBO = glGenBuffers(1)
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

    # Draw and Run
    glViewport(0, 0, width, height)
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)

    # glBindVertexArray(VAO)
    # glEnableVertexAttribArray(0)
    # glEnableVertexAttribArray(1)

    glUniformMatrix4fv(glGetUniformLocation(program, 'transform'), 1, GL_FALSE, transform)

    # for i in range(0,len(index_list),3):
    #     # glDrawArrays(GL_POLYGON, index_list[i], index_list[i+1] )
    print(len(vertices))

    glDrawElements(GL_TRIANGLES, len(vertices), GL_UNSIGNED_INT, indices)

    pygame.display.flip()

def startShowcase(car_obj):
    pygame.init()
    pygame.display.set_mode((width,height),pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.display.set_caption("OpenXV")
    clock = pygame.time.Clock()
    done = False
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45,640.0/480.0,0.1,200.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    running = True
    angle = 0
    matrix = transformations.identity_matrix()

    while running:
    #     events = pygame.event.get()
        
    #     keys = pygame.key.get_pressed()
    #     if keys[K_LEFT] or keys[K_RIGHT] or keys[K_UP] or keys[K_DOWN]:
    #         dx, dy = (0, 0)
    #         if keys[K_LEFT]:
    #             dx = 0.1
    #         elif keys[K_RIGHT]:
    #             dx = -0.1
    #         if keys[K_UP]:
    #             dy = -0.1
    #         elif keys[K_DOWN]:
    #             dy = 0.1
    #         trans = transformations.translation_matrix([dx, dy, 0])
    #         matrix = numpy.matmul(trans, matrix)
        
    #     if keys[K_w] or keys[K_a] or keys[K_s] or keys[K_d]:
    #         ai, aj = (0, 0)
    #         if keys[K_a]:
    #             aj = -DEGREE
    #         elif keys[K_d]:
    #             aj = DEGREE            
    #         if keys[K_w]:
    #             ai = DEGREE
    #         elif keys[K_s]:
    #             ai = -DEGREE
    #         trans = transformations.euler_matrix(ai, aj, 0)
    #         matrix = numpy.matmul(trans, matrix)

    #     if keys[K_r] or keys[K_f]:
    #         scale = 1
    #         if keys[K_r]:
    #             scale = 1.1
    #         if keys[K_f]:
    #             scale = 0.9
    #         trans = transformations.scale_matrix(scale)
    #         matrix = numpy.matmul(trans, matrix)

    #     # Check if certain region is pressed with mouse
    #     if pygame.mouse.get_pressed()[0]:
    #         mouseX, mouseY = pygame.mouse.get_pos()
    #         ai, aj = (0, 0)

    #         if mouseX < 100:
    #             aj = -DEGREE
    #         elif mouseX > (width - 100):
    #             aj = DEGREE
            
    #         if mouseY < 100:
    #             ai = DEGREE
    #         elif mouseY > (height - 100):
    #             ai = -DEGREE

    #         trans = transformations.euler_matrix(ai, aj, 0)
    #         matrix = numpy.matmul(trans, matrix)

    #     # wait for exit
    #     for event in events:
    #         if event.type == pygame.QUIT: # If user clicked close
    #             done = True
    #         if event.type == KEYDOWN:
    #             if event.key == K_ESCAPE:
    #                 pygame.quit()
    #                 running = False
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             scale = 1
    #             if event.button == 4:
    #                 scale = 1.1
    #             if event.button == 5:
    #                 scale = 0.9

    #             trans = transformations.scale_matrix(scale)
    #             matrix = numpy.matmul(trans, matrix)

    #     car_obj.render_scene()

        car_obj.render_scene()
        pygame.display.flip()

if __name__ == '__main__':
    print("Hi from car.py")
